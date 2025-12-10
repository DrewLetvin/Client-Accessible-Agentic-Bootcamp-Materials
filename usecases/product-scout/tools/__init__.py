"""
tools

Lightweight, composable tools for product lookup and safety checks.

Exports
-------
Functions:
- off_search_tool        # OFF fuzzy search → candidate barcodes
- off_product_tool       # OFF product by barcode (allergens, etc.)
- fda_recalls_tool       # openFDA Food Enforcement recalls
- wikidata_gtin_tool     # SPARQL lookup for GTINs (P3962)
- schema_org_gtin_tool   # Extract GTINs from schema.org JSON-LD on a PDP

Schemas:
- OFFSearchInput, OFFSearchOutput, OFFSearchHit
- OFFProductInput, OFFProductOutput
- FDARecallsInput, FDARecallsOutput, FDARecall
- WikidataGTINInput, WikidataGTINOutput, WikidataGTINHit
- SchemaOrgGTINInput, SchemaOrgGTINOutput

Notes
-----
- Set env var PRODUCT_TOOLS_UA before import to override the default User-Agent.
- Treat barcodes as strings (leading zeros).
"""

from .off import off_search_tool, off_product_tool
from .fda import fda_recalls_tool
from .wikidata import wikidata_gtin_tool
from .schema_gtin import schema_org_gtin_tool
from .http import DEFAULT_UA

from .schemas import (
    OFFSearchInput, OFFSearchOutput, OFFSearchHit,
    OFFProductInput, OFFProductOutput,
    FDARecallsInput, FDARecallsOutput, FDARecall,
    WikidataGTINInput, WikidataGTINOutput, WikidataGTINHit,
    SchemaOrgGTINInput, SchemaOrgGTINOutput,
)

__all__ = [
    # functions
    "off_search_tool", "off_product_tool",
    "fda_recalls_tool",
    "wikidata_gtin_tool",
    "schema_org_gtin_tool",
    # helpers
    "DEFAULT_UA",
    # schemas
    "OFFSearchInput", "OFFSearchOutput", "OFFSearchHit",
    "OFFProductInput", "OFFProductOutput",
    "FDARecallsInput", "FDARecallsOutput", "FDARecall",
    "WikidataGTINInput", "WikidataGTINOutput", "WikidataGTINHit",
    "SchemaOrgGTINInput", "SchemaOrgGTINOutput",
]

__version__ = "0.1.0"
