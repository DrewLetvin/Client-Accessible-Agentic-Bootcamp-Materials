# product_tools/wikidata.py
import requests
from typing import Dict, List, Set
from ibm_watsonx_orchestrate.agent_builder.tools import tool

WD_API = "https://www.wikidata.org/w/api.php"
HEADERS = {
    "Accept": "application/json",
    "User-Agent": "AndreCareBot/0.1 (andretost@yahoo.com)"  # put your contact/app here
}

@tool()
def wikidata_gtin_tool(label: str, brand: str = "", limit: int = 20, timeout: int = 30, **_) -> dict:
    """
    TOOL: Wikidata GTINs via MediaWiki API (GTIN-only search with fallback)

    Strategy
    --------
    A) action=query&list=search with srsearch = haswbstatement:P3962 <label> [brand]
       → returns Q-IDs that *have* a GTIN (P3962).
    B) Fallback: wbsearchentities(label [brand]) → Q-IDs → filter to those with P3962.
    Then wbgetentities to fetch labels, P3962 GTINs, and brand/manufacturer (P1716/P176) labels.

    Inputs
    - label: str          e.g., "Nutella"
    - brand: str = ""     e.g., "Ferrero"
    - limit: int = 20     1..100
    - timeout: int = 30   read timeout seconds

    Output
    { "hits": [ { "item": IRI, "label": str, "gtin": str, "brand_label": str|None }, ... ],
      "note": "which path / counts" }
    """
    # normalize
    try:
        limit = max(1, min(int(limit), 100))
    except Exception:
        limit = 20
    try:
        timeout = int(timeout)
    except Exception:
        timeout = 30

    def _get(params: Dict[str, str]) -> dict:
        r = requests.get(WD_API, params=params, headers=HEADERS, timeout=(5, timeout))
        r.raise_for_status()
        return r.json()

    # ----- A) GTIN-only search (CirrusSearch) -----
    # Build a search that *requires* haswbstatement:P3962 and also matches the label (and brand if given)
    sr_terms = ["haswbstatement:P3962"]
    if label:
        sr_terms.append(label)
    if brand:
        sr_terms.append(brand)
    srsearch = " ".join(sr_terms)

    qids: List[str] = []
    try:
        a = _get({
            "action": "query",
            "list": "search",
            "srsearch": srsearch,
            "srnamespace": "0",
            "srlimit": str(limit),
            "format": "json",
        })
        for hit in a.get("query", {}).get("search", []) or []:
            # Titles are like "Q829080"
            t = hit.get("title")
            if isinstance(t, str) and t.startswith("Q"):
                qids.append(t)
    except Exception:
        # If A fails, we’ll rely on B
        pass

    # ----- B) Fallback: plain wbsearchentities → filter later -----
    if not qids:
        try:
            s = _get({
                "action": "wbsearchentities",
                "search": f"{label} {brand}".strip(),
                "language": "en",
                "type": "item",
                "limit": str(limit),
                "format": "json",
            })
            qids = [h["id"] for h in (s.get("search") or []) if "id" in h][:limit]
            note = "fallback wbsearchentities"
        except Exception as e:
            return {"hits": [], "note": f"wbsearchentities failed: {e.__class__.__name__}"}
    else:
        note = "query search haswbstatement:P3962"

    if not qids:
        return {"hits": [], "note": f"{note} → no Q-IDs"}

    # ----- Fetch entities → labels + claims -----
    try:
        e = _get({
            "action": "wbgetentities",
            "ids": "|".join(qids),
            "props": "labels|claims",
            "languages": "en",
            "format": "json",
        })
    except Exception as e:
        return {"hits": [], "note": f"wbgetentities failed: {e.__class__.__name__}"}

    entities = (e.get("entities") or {})
    brand_qids: Set[str] = set()

    def _label_of(ent: dict) -> str:
        return (ent.get("labels", {}).get("en", {}) or {}).get("value", "")

    tmp_rows = []
    for qid, ent in entities.items():
        if not isinstance(ent, dict):
            continue
        claims = ent.get("claims") or {}
        # Collect GTINs (P3962)
        gtins = []
        for cl in claims.get("P3962", []) or []:
            dv = (cl.get("mainsnak", {}).get("datavalue") or {}).get("value")
            if isinstance(dv, str):
                gtins.append(dv.strip())
        if not gtins:
            continue  # keep only items that really have GTINs

        # Gather brand/manufacturer item QIDs for label resolution
        bq: Set[str] = set()
        for pid in ("P1716", "P176"):
            for cl in claims.get(pid, []) or []:
                dv = (cl.get("mainsnak", {}).get("datavalue") or {}).get("value")
                if isinstance(dv, dict) and dv.get("entity-type") == "item":
                    bqid = "Q" + str(dv.get("numeric-id"))
                    bq.add(bqid)
                    brand_qids.add(bqid)

        tmp_rows.append((qid, _label_of(ent), gtins, bq))

    if not tmp_rows:
        return {"hits": [], "note": f"{note} → entities had no P3962"}

    # Resolve brand/manufacturer labels (if any)
    brand_labels: Dict[str, str] = {}
    if brand_qids:
        try:
            b = _get({
                "action": "wbgetentities",
                "ids": "|".join(sorted(brand_qids)),
                "props": "labels",
                "languages": "en",
                "format": "json",
            })
            for bqid, bent in (b.get("entities") or {}).items():
                brand_labels[bqid] = _label_of(bent)
        except Exception:
            pass

    # Build rows + optional brand filter
    brand_lc = (brand or "").strip().lower()
    rows = []
    for qid, lbl, gtins, bq in tmp_rows:
        blist = [brand_labels.get(x) for x in bq if brand_labels.get(x)]
        brand_label = blist[0] if blist else None
        if brand_lc:
            if brand_lc not in lbl.lower() and not any(brand_lc in (bl or "").lower() for bl in blist):
                continue
        for g in gtins:
            rows.append({
                "item": f"https://www.wikidata.org/entity/{qid}",
                "label": lbl,
                "gtin": g,
                "brand_label": brand_label,
            })

    return {"hits": rows[:limit], "note": note}

if __name__ == "__main__":
    import os, json, time, argparse, traceback

    parser = argparse.ArgumentParser(description="Test wikidata_gtin_tool from the CLI.")
    parser.add_argument("--label", required=True, help='e.g. "LEGO 10280" or "iPhone 14 Pro"')
    parser.add_argument("--brand", default="", help='e.g. "LEGO" or "Apple"')
    parser.add_argument("--limit", type=int, default=10)
    parser.add_argument("--timeout", type=int, default=30)
    parser.add_argument("--debug", action="store_true", help="Print full JSON")
    args = parser.parse_args()

    # Let you override UA quickly:  WD_UA="MyApp/1.0 (email@domain)" python wikidata.py ...
    if "WD_UA" in os.environ:
        try:
            # HEADERS is defined above in this module
            HEADERS["User-Agent"] = os.environ["WD_UA"]
        except Exception:
            pass

    print(f"[wikidata] endpoint={WD_API}  label={args.label!r}  brand={args.brand!r}  limit={args.limit}  timeout={args.timeout}")
    t0 = time.time()
    try:
        out = wikidata_gtin_tool(label=args.label, brand=args.brand, limit=args.limit, timeout=args.timeout)
        dt = time.time() - t0
        print(f"[wikidata] elapsed={dt:.2f}s  note={out.get('note')!r}")
        hits = out.get("hits", [])
        if args.debug:
            print(json.dumps(out, indent=2, ensure_ascii=False))
        else:
            if not hits:
                print("No hits.")
            for h in hits:
                print(f"{h.get('gtin','')}  | {h.get('label','')}  | {h.get('brand_label') or ''}  | {h.get('item','')}")
    except Exception as e:
        print("[wikidata] ERROR:", repr(e))
        traceback.print_exc()
        raise

