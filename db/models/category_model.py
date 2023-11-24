from pydantic import BaseModel, Field
from bson import ObjectId
from typing import Optional


class Category(BaseModel):
    id: Optional[str] = Field(default=None)
    name: str

    
    
def category_scheme(category) -> dict:
    return {
        "id" : str(category["_id"]),
        "name" : category["name"],
    }