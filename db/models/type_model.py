from pydantic import BaseModel, Field
from bson import ObjectId
from typing import Optional
from datetime import datetime


class Type(BaseModel):
    id: Optional[str] = Field(default=None)
    type: str
    image: Optional[str] = Field(default = "/static/images/new_product_logo.png")
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()

    
    
def type_scheme(type) -> dict:
    return {
        "id" : str(type["_id"]),
        "type" : type["type"],
        "image" : type["image"],
    }