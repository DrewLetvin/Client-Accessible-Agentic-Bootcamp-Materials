import re, json, requests
from ibm_watsonx_orchestrate.agent_builder.tools import tool

@tool()
def schema_org_gtin_tool(url: str, **_) -> dict:
    """
    TOOL: schema.org/Product JSON-LD – Extract GTINs from a product page URL

    Inputs
    - url: str (product detail page likely to include JSON-LD)

    Output (dict)
    { "gtins": [str, ...] }
    """
    html = requests.get(url, timeout=20).text
    blobs = re.findall(r'<script type="application/ld\\+json">(.*?)</script>', html, re.S | re.I)
    gtins = set()

    def walk(x):
        if isinstance(x, dict):
            for k, v in x.items():
                if k.lower() in {"gtin", "gtin12", "gtin13", "gtin14"} and isinstance(v, str):
                    gtins.add(v.strip())
                walk(v)
        elif isinstance(x, list):
            for i in x:
                walk(i)

    for b in blobs:
        try:
            data = json.loads(b)
            walk(data)
        except Exception:
            continue
    return {"gtins": sorted(gtins)}
