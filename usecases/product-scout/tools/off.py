# product_tools/off.py
from typing import List
import requests
from tools.http import http_get_json_with_retries as GET
from tools.http import DEFAULT_UA, http_get_json
from ibm_watsonx_orchestrate.agent_builder.tools import tool

def _mk_hdr():
    return {"User-Agent": DEFAULT_UA, "Accept": "application/json"}

def _to_hits(products):
    out = []
    for p in products or []:
        code = p.get("code")
        if not code:
            continue
        out.append({
            "code": code,
            "name": p.get("product_name"),
            "brand": (p.get("brands") or "").split(",")[0].strip() if p.get("brands") else None,
            "quantity": p.get("quantity"),
            "countries": p.get("countries_tags_en") or p.get("countries_tags"),
        })
    return out


@tool()
def off_search_tool(query: str, page_size: int = 20, lc: str = "en", cc: str = "us", **_) -> dict:
    """
    Open Food Facts – Fuzzy search → candidate barcodes. If not passed, country code defaults to "us" and language code defaults to "en".

    Inputs
    - query: str, e.g. "nutella hazelnut spread"
    - page_size: int (1..100, default 20)
    - lc: str, language code, default "en"
    - cc: str, country code, default "us"

    Returns 
    - dict: { "hits": [...], "path": "v1|sal|v2", "query_used": "<debug string>" }
    """
    # --- 1) v1 full-text (preferred for FT), force fresh cache and locale bias
    v1 = "https://world.openfoodfacts.org/cgi/search.pl"
    p1 = {
        "search_terms": query,
        "search_simple": "1",
        "action": "process",
        "page_size": str(page_size),
        "json": "1",
        "nocache": "1",
        "lc": lc,
        "cc": cc,
    }
    j1 = GET(v1, params=p1, headers=_mk_hdr()) or {}
    hits1 = _to_hits(j1.get("products", []))
    if hits1:
        return {"hits": hits1, "path": "v1", "query_used": f"{v1}?…"}

    # --- 2) Search-a-licious (newer FT backend)
    sal = "https://search.openfoodfacts.org/cgi/search.pl"
    p2 = dict(p1)  # same params are accepted here
    j2 = GET(sal, params=p2, headers=_mk_hdr()) or {}
    hits2 = _to_hits(j2.get("products", []))
    if hits2:
        return {"hits": hits2, "path": "sal", "query_used": f"{sal}?…"}

    # --- 3) v2 filter fallback, bias to US when possible
    v2 = "https://world.openfoodfacts.org/api/v2/search"
    p3 = {
        "fields": "code,product_name,brands,quantity,countries_tags_en",
        "page_size": str(page_size),
        "countries_tags_en": "United States",
    }
    j3 = GET(v2, params=p3, headers=_mk_hdr()) or {}
    hits3 = _to_hits(j3.get("products", []))
    return {"hits": hits3, "path": "v2", "query_used": f"{v2}?…"}

@tool()
def off_product_tool(barcode: str, **_) -> dict:
    """
    TOOL: Open Food Facts – Product by barcode

    Inputs
    - barcode: str (GTIN/UPC/EAN)

    Output (dict)
    { "found": bool, "code": str, "name": str|None, "brand": str|None,
      "quantity": str|None, "allergens": [str], "traces": [str],
      "ingredients_text": str|None, "nutri_grade": str|None,
      "labels": [str], "raw": { ... } }
    """
    fields = (
        "code,product_name,generic_name,brands,quantity,"
        "allergens_tags,traces,traces_tags,ingredients_text,"
        "nutrition_grades,labels_tags"
    )

    def fetch(code: str):
        url = f"https://world.openfoodfacts.org/api/v2/product/{code}.json"
        try:
            return http_get_json(url, params={"fields": fields}, headers={"User-Agent": DEFAULT_UA})
        except requests.HTTPError as e:
            if e.response is not None and e.response.status_code == 404:
                return None  # treat as not found
            raise

    # 1) Try as-is
    j = fetch(barcode)
    tried_code = barcode

    # 2) If not found and looks like UPC-A, try EAN-13 with leading 0
    if j is None and try_upc_to_ean and len(barcode) == 12 and not barcode.startswith("0"):
        alt = "0" + barcode
        j = fetch(alt)
        tried_code = alt if j is not None else barcode

    # 3) Not found after attempts → return graceful miss
    if j is None or j.get("status") != 1 or "product" not in j:
        return {"found": False, "code": tried_code}

    p = j["product"]

    def tidy_tags(tags):
        if not tags:
            return []
        return [t.split(":", 1)[-1].replace("-", " ").title() for t in tags]

    allergens = tidy_tags(p.get("allergens_tags"))
    traces = tidy_tags(p.get("traces_tags")) or [
        t.strip().title() for t in (p.get("traces") or "").split(",") if t.strip()
    ]
    name = p.get("product_name") or p.get("generic_name")

    return {
        "found": True,
        "code": j.get("code") or tried_code,
        "name": name,
        "brand": (p.get("brands") or "").split(",")[0].strip() if p.get("brands") else None,
        "quantity": p.get("quantity"),
        "allergens": allergens,
        "traces": traces,
        "ingredients_text": p.get("ingredients_text"),
        "nutri_grade": p.get("nutrition_grades"),
        "labels": p.get("labels_tags") or [],
        "raw": p,
    }

if __name__ == "__main__":
    import argparse, json, time, traceback, re

    def _tokenize(s: str) -> list[str]:
        return re.findall(r"[a-z0-9]+", (s or "").lower())

    def pick_best_off_hit(user_query: str, hits: list[dict], min_score: int = 2) -> dict | None:
        """
        Generic, brand-agnostic scorer:
        - token overlap between user query and (brand + name)
        - small bonus if the full query phrase appears inside brand+name
        """
        qtokens = set(t for t in _tokenize(user_query) if len(t) >= 3)
        phrase = (user_query or "").strip().lower()

        def score(h: dict) -> int:
            name = (h.get("name") or "").lower()
            brand = (h.get("brand") or "").lower()
            text = f"{brand} {name}"
            htoks = set(_tokenize(text))
            s = len(qtokens & htoks)                       # token overlap
            if len(phrase) >= 8 and phrase in text:
                s += 3                                     # phrase bonus
            return s

        best = max(hits or [], key=score, default=None)
        return best if (best and score(best) >= min_score) else None

    parser = argparse.ArgumentParser(description="OFF search → OFF product smoke test")
    parser.add_argument("--query", required=True, help='e.g. "Ben & Jerry\'s Cherry Garcia"')
    parser.add_argument("--page-size", type=int, default=20)
    parser.add_argument("--lc", default="en")
    parser.add_argument("--cc", default="us")
    parser.add_argument("--picker", choices=["best", "first"], default="best",
                        help="how to choose a hit before fetching product")
    parser.add_argument("--debug", action="store_true")
    args = parser.parse_args()

    print(f"[OFF] query={args.query!r} page_size={args.page_size} lc={args.lc} cc={args.cc}")
    t0 = time.time()
    try:
        search_out = off_search_tool(query=args.query, page_size=args.page_size, lc=args.lc, cc=args.cc)
        dt = time.time() - t0
        hits = (search_out or {}).get("hits", []) or []
        path = (search_out or {}).get("path")
        tried = (search_out or {}).get("queries_tried", [])
        print(f"[OFF search] elapsed={dt:.2f}s  path={path!r}  hits={len(hits)}")
        if tried:
            print("[OFF search] queries_tried:")
            for q in tried:
                print("  -", q)

        if not hits:
            print("No search hits. Exiting.")
            raise SystemExit(0)

        # choose a hit
        if args.picker == "first":
            chosen = hits[0]
        else:
            chosen = pick_best_off_hit(args.query, hits) or hits[0]

        print("[OFF pick] →", {
            "code": chosen.get("code"),
            "name": chosen.get("name"),
            "brand": chosen.get("brand"),
            "quantity": chosen.get("quantity"),
        })

        # fetch product detail by barcode
        t1 = time.time()
        prod = off_product_tool(barcode=chosen["code"])
        dt2 = time.time() - t1

        if not (prod or {}).get("found"):
            print(f"[OFF product] elapsed={dt2:.2f}s  NOT FOUND for code={chosen['code']}")
            # still exit 0 — this is a valid outcome for some barcodes
            raise SystemExit(0)

        # pretty print a compact summary
        summary = {
            "code": prod.get("code"),
            "name": prod.get("name"),
            "brand": prod.get("brand"),
            "quantity": prod.get("quantity"),
            "nutri_grade": prod.get("nutri_grade"),
            "allergens": prod.get("allergens"),
            "traces": prod.get("traces"),
            "labels": prod.get("labels"),
        }
        print(f"[OFF product] elapsed={dt2:.2f}s")
        if args.debug:
            print(json.dumps(prod, indent=2, ensure_ascii=False))
        else:
            print(json.dumps(summary, indent=2, ensure_ascii=False))

    except Exception as e:
        print("[OFF] ERROR:", repr(e))
        traceback.print_exc()
        raise
