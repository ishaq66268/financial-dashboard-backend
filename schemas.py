from pydantic import BaseModel, Field
from datetime import date
from typing import List

class EntryIn(BaseModel):
    date: date
    counter_amount: float = Field(ge=0)
    material_cost: float = Field(ge=0)
    savings: float = Field(ge=0)

class EntryOut(EntryIn):
    id: str  # MongoDB _id converted to string
    profit: float

class Metrics(BaseModel):
    total_counter_amount: float
    total_material_cost: float
    total_savings: float
    total_profit: float
    entries: List[EntryOut]
