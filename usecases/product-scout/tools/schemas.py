# product_tools/schemas.py
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class OFFSearchInput(BaseModel):
    query: str = Field(..., description="Free-text product search, e.g., 'nutella hazelnut spread'")
    page_size: int = Field(20, ge=1, le=100)

class OFFSearchHit(BaseModel):
    code: str
    name: Optional[str] = None
    brand: Optional[str] = None
    quantity: Optional[str] = None
    countries: Optional[List[str]] = None

class OFFSearchOutput(BaseModel):
    hits: List[OFFSearchHit]

class OFFProductInput(BaseModel):
    barcode: str = Field(..., description="GTIN/UPC/EAN as digits")

class OFFProductOutput(BaseModel):
    found: bool
    code: str
    name: Optional[str] = None
    brand: Optional[str] = None
    quantity: Optional[str] = None
    allergens: List[str] = []
    traces: List[str] = []
    nutri_grade: Optional[str] = None
    labels: List[str] = []
    ingredients_text: Optional[str] = None
    raw: Dict[str, Any] = {}

class FDARecallsInput(BaseModel):
    barcode: str
    brand: Optional[str] = ""
    name: Optional[str] = ""
    limit: int = Field(5, ge=1, le=50)

class FDARecall(BaseModel):
    recall_number: Optional[str] = None
    classification: Optional[str] = None
    recall_initiation_date: Optional[str] = None
    recalling_firm: Optional[str] = None
    status: Optional[str] = None
    product_description: Optional[str] = None
    code_info: Optional[str] = None

class FDARecallsOutput(BaseModel):
    results: List[FDARecall] = []

class WikidataGTINInput(BaseModel):
    label: str = Field(..., description="Product label or name to search in Wikidata")
    brand: Optional[str] = Field("", description="Optional brand to narrow results")
    limit: int = Field(20, ge=1, le=100)

class WikidataGTINHit(BaseModel):
    item: str
    label: str
    gtin: str
    brand_label: Optional[str] = None

class WikidataGTINOutput(BaseModel):
    hits: List[WikidataGTINHit] = []

class SchemaOrgGTINInput(BaseModel):
    url: str

class SchemaOrgGTINOutput(BaseModel):
    gtins: List[str] = []
