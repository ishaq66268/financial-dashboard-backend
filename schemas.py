from pydantic import BaseModel
from datetime import date
from typing import Optional

class EntryIn(BaseModel):
    date: date
    counter_amount: float
    material_cost: float
    savings: float

class EntryOut(EntryIn):
    id: str
    profit: float
