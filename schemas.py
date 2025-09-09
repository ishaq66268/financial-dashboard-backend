from pydantic import BaseModel, Field
from datetime import date
from typing import Literal, Optional, List

class EntryIn(BaseModel):
    date: date
    counter_amount: float = Field(ge=0)
    material_cost: float = Field(ge=0)
    savings: float = Field(ge=0)

class EntryOut(EntryIn):
    profit: float

class Metrics(BaseModel):
    total_counter_amount: float
    total_material_cost: float
    total_savings: float
    total_profit: float
    entries: list[EntryOut]
