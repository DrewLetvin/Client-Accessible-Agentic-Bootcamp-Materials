#!/usr/bin/env python3
import os, time, random
import requests
from urllib.parse import quote_plus

OFF_BASE = "https://world.openfoodfacts.org"
FDA_BASE = "https://api.fda.gov"

UA = "AndreCareBot/0.1 (andre@example.com)"  # set your own UA

def _get(url, headers=None, params=None, timeout=10):
    h = {"Accept": "application/json"}
    if headers:
        h.update(headers)
    r = requests.get(url, headers=h, params=params, timeout=timeout)
    r.raise_for_status()
    return r.json()

def _get_with_retries(url, headers=None, params=None, timeout=10, max_attempts=4):
    """Retry on 429/5xx with exponential backoff + jitter."""
    attempt = 0
    while True:
        try:
            return _get(url, headers=headers, params=params, timeout=timeout)
        except requests.HTTPError as e:
            status = e.response.status_code if e.response is not None else None
            if status in (429, 500, 502, 503, 504) and attempt < max_attempts - 1:
                sleep = (2 ** attempt) * 0.7 + random.random() * 0.3
                attempt += 1
                print(f"openFDA HTTP {status}; retrying in {sleep:.1f}s (attempt {attempt}/{max_attempts})")
                time.sleep(sleep)
                continue
            if status == 404:
                return {}
            # Non-retryable or retries exhausted → bubble up
            raise
        except requests.RequestException as e:
            if attempt < max_attempts - 1:
                sleep = (2 ** attempt) * 0.7 + random.random() * 0.3
                attempt += 1
                print(f"openFDA network error {e.__class__.__name__}; retrying in {sleep:.1f}s (attempt {attempt}/{max_attempts})")
                time.sleep(sleep)
                continue
            raise

def off_get_product(barcode: str) -> dict:
    """Fetches core product info from Open Food Facts v2."""
    fields = (
        "code,product_name,generic_name,brands,quantity,"
        "allergens_tags,traces,traces_tags,ingredients_text,"
        "nutrition_grades,labels_tags"
    )
    url = f"{OFF_BASE}/api/v2/product/{barcode}.json"
    j = _get(url, headers={"User-Agent": UA}, params={"fields": fields})
    if j.get("status") != 1 or "product" not in j:
        return {"found": False, "code": barcode}
    p = j["product"]
    def clean_tags(tags):
        if not tags:
            return []
        return [t.split(":", 1)[-1].replace("-", " ").title() for t in tags]

    allergens = clean_tags(p.get("allergens_tags"))
    traces = clean_tags(p.get("traces_tags")) or [
        t.strip().title() for t in (p.get("traces") or "").split(",") if t.strip()
    ]
    name = p.get("product_name") or p.get("generic_name") or "(Unnamed product)"
    return {
        "found": True,
        "code": j.get("code") or barcode,
        "name": name,
        "brand": (p.get("brands") or "").split(",")[0].strip(),
        "quantity": p.get("quantity"),
        "allergens": allergens,
        "traces": traces,
        "ingredients_text": p.get("ingredients_text"),
        "nutri_grade": p.get("nutrition_grades"),
        "labels": p.get("labels_tags") or [],
        "raw": p,
    }

def fda_food_recalls_lookup(barcode: str, brand: str = "", name: str = "", limit: int = 5) -> list:
    """
    Query openFDA Food Enforcement recalls.
    Strategy:
      1) Try barcode (quoted) in code_info OR product_description.
      2) Fallback to brand + product name tokens (loose match).
      Returns [] on 404/no results or if the API is flaky after retries.
    """
    api_key = os.getenv("OPENFDA_API_KEY")  # optional
    def q(expr):
        url = f"{FDA_BASE}/food/enforcement.json"
        params = {"search": expr, "limit": str(limit), "sort": "report_date:desc"}
        if api_key:
            params["api_key"] = api_key
        j = _get_with_retries(url, params=params, timeout=20)
        return j.get("results", []) if j else []

    # 1) Barcode exact phrase (safer than unquoted)
    quoted = f'"{barcode}"'
    expr = f'code_info:{quote_plus(quoted)}+OR+product_description:{quote_plus(quoted)}'
    results = q(expr)
    if results:
        return results

    # 2) Brand + first few informative tokens from product name
    tokens = [t for t in name.replace(",", " ").split() if len(t) > 2][:4]
    terms = []
    if brand:
        terms.append(f'product_description:"{brand}"')
        terms.append(f'recalling_firm:"{brand}"')
    for t in tokens:
        terms.append(f'product_description:"{t}"')
    if terms:
        expr = "+AND+".join(terms)
        return q(expr)

    return []

def summarize(barcode: str):
    prod = off_get_product(barcode)
    if not prod["found"]:
        print(f"OFF: product {barcode} not found.")
        return

    print(f"Product: {prod['name']}  (Brand: {prod['brand'] or '—'})")
    print(f"Barcode: {prod['code']}  Qty: {prod['quantity'] or '—'}  Nutri-Score: {prod['nutri_grade'] or '—'}")
    if prod["allergens"]:
        print("Allergens:", ", ".join(prod["allergens"]))
    else:
        print("Allergens: none listed")
    if prod["traces"]:
        print("May contain traces of:", ", ".join(prod["traces"]))

    try:
        recalls = fda_food_recalls_lookup(barcode, prod["brand"], prod["name"], limit=5)
    except requests.HTTPError as e:
        # Final safety net: don't crash your CX flow on FDA hiccups
        print(f"openFDA error after retries ({e}); treating as no recalls available right now.")
        recalls = []

    if not recalls:
        print("openFDA Recalls: none found or service temporarily unavailable.")
    else:
        print(f"openFDA Recalls (latest {len(recalls)}):")
        for r in recalls:
            print(f"- {r.get('recall_number')} | {r.get('classification')} | {r.get('recall_initiation_date')} "
                  f"| {r.get('recalling_firm')} | {r.get('status')}")
            desc = (r.get("product_description") or "").strip()
            if desc:
                print(f"  {desc[:160]}{'…' if len(desc) > 160 else ''}")

if __name__ == "__main__":
    summarize("3017620422003")
