from datetime import datetime
from pydantic import BaseModel
from typing import List, Dict


class ProductSchema(BaseModel):
    name: str
    product_class: str
    description: str
    images: List[Dict]
    created_at: datetime = None
    updated_at: datetime = None
    user_id: str

    class Config:
        orm_mode = True
