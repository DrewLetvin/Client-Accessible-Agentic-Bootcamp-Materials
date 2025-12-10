#!/usr/bin/env python3
import os, time
from tools.off import off_search_tool, off_product_tool
from tools.fda import fda_recalls_tool

# Strongly recommended for OFF
os.environ.setdefault("PRODUCT_TOOLS_UA", "AndreCareBot/0.1 (andre@example.com)")

QUERIES = [
    "oreo double stuf 15.35 oz",
    "heinz ketchup 38 oz",
    "chobani greek yogurt strawberry 5.3 oz",
    "barilla spaghetti 1 lb",
    "coca cola 12 oz",
    "nutella hazelnut spread 26.5 oz",
]

def run_case(q: str):
    print(f"\n=== {q} ===")
    t0 = time.time()
    s = off_search_tool(query=q, page_size=5)
    hits = s.get("hits", [])
    if not hits:
        print("OFF search: no hits")
        return
    best = hits[0]
    print("OFF search →", best)
    p = off_product_tool(barcode=best["code"])
    if not p.get("found"):
        print("OFF product: not found (still testing FDA)")
        brand = best.get("brand") or ""
        name = best.get("name") or ""
    else:
        print("OFF product →", {k: p.get(k) for k in ["code","name","brand","nutri_grade","allergens","traces"]})
        brand = p.get("brand") or (best.get("brand") or "")
        name = p.get("name") or (best.get("name") or "")
    r = fda_recalls_tool(barcode=best["code"], brand=brand, name=name, limit=5)
    print("FDA recalls:", len(r.get("results", [])))
    for rr in r.get("results", [])[:3]:
        print(" -", rr.get("recall_number"), rr.get("classification"), rr.get("recall_initiation_date"), rr.get("recalling_firm"))

    print(f"elapsed: {time.time()-t0:.2f}s")

if __name__ == "__main__":
    for q in QUERIES:
        run_case(q)
