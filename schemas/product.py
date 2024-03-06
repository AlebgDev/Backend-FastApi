from typing import Optional
from pydantic import BaseModel

class Product(BaseModel):
    id: Optional[int] = None
    name: str
    description: str
    price: float