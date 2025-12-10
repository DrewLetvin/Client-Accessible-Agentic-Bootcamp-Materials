import os, re, datetime as dt, requests
from ibm_watsonx_orchestrate.agent_builder.tools import tool
from tools.http import http_get_json_with_retries

FDA_BASE = "https://api.fda.gov"

def _digits(s: str) -> str:
    return re.sub(r"\D", "", s or "")

def _gtin_variants(raw: str) -> list[str]:
    d = _digits(raw)
    if not d: return []
    out = {d}
    if len(d) == 13 and d.startswith("0"): out.add(d[1:])    # UPC-A
    if len(d) == 12: out.add("0" + d)                        # EAN-13
    if len(d) in (12, 13): out.add(d.rjust(14, "0"))         # GTIN-14
    return list(out)

@tool()
def fda_recalls_tool(
    barcode: str | None = "",
    brand: str | None = "",
    name: str | None = "",
    limit: int | str = 5,
    days_back: int | str = 180,
    **_
) -> dict:
    """
    openFDA Food Enforcement: find recalls by barcode (UPC/EAN/GTIN) OR by product name/brand.
    - No 'sort=' (endpoint rejects it intermittently).
    - If barcode is absent, uses phrase + token search across multiple fields within a date window.
    Returns: {
      "results": [...],
      "query_used": str|None,
      "queries_tried": [str],
      "variants_tried": [str],
      "note": str|None
    }
    """
    try: limit = int(limit)
    except: limit = 5
    try: days_back = int(days_back)
    except: days_back = 180

    base_url = f"{FDA_BASE}/food/enforcement.json"
    api_key = os.getenv("OPENFDA_API_KEY")

    def call(expr: str) -> list[dict]:
        params = {"search": expr, "limit": str(limit)}
        if api_key: params["api_key"] = api_key
        try:
            j = http_get_json_with_retries(base_url, params=params) or {}
            return j.get("results", []) or []
        except requests.HTTPError as e:
            if e.response is not None and e.response.status_code in (400, 404):
                return []
            raise

    queries_tried = []
    variants = _gtin_variants(barcode) if barcode else []

    # 1) Barcode-first (if provided)
    for v in variants:
        expr = f'code_info:"{v}" OR product_description:"{v}"'
        queries_tried.append(expr)
        res = call(expr)
        if res:
            return {"results": res, "query_used": expr, "queries_tried": queries_tried, "variants_tried": variants}

    # 2) Phrase + token search within date window (works with name/brand only)
    end = dt.date.today()
    start = end - dt.timedelta(days=days_back)
    window = f"report_date:[{start:%Y%m%d} TO {end:%Y%m%d}]"

    phrases = [x.strip() for x in (brand or "", name or "") if x and x.strip()]
    tokens  = [t.lower() for t in re.findall(r"[A-Za-z0-9]+", f"{brand or ''} {name or ''}") if len(t) >= 3]

    if phrases or tokens:
        parts = []
        for ph in phrases:
            qph = f'"{ph}"'
            parts += [f"product_description:{qph}", f"reason_for_recall:{qph}", f"recalling_firm:{qph}"]
        if tokens:
            kw = " AND ".join(tokens)
            parts += [f"product_description:({kw})", f"reason_for_recall:({kw})", f"recalling_firm:({kw})"]
        expr2 = f"{window} AND (" + " OR ".join(parts) + ")"
        queries_tried.append(expr2)
        res2 = call(expr2)
        if res2:
            return {"results": res2, "query_used": expr2, "queries_tried": queries_tried, "variants_tried": variants}

    # 3) Last resort: date window only (keeps UX alive)
    expr3 = window
    queries_tried.append(expr3)
    res3 = call(expr3)
    note = None
    if res3:
        note = "no direct match; returned recent recalls in window"

    return {
        "results": res3,
        "query_used": expr3 if res3 else None,
        "queries_tried": queries_tried,
        "variants_tried": variants,
        "note": note or "no hits after barcode + keyword/date fallback",
    }
