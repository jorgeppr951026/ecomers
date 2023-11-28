from pydantic import BaseModel, Field
from bson import ObjectId
from typing import Optional
from datetime import datetime

class Category(BaseModel):
    id: Optional[str] = Field(default=None)
    name: str
    image: Optional[str] = Field(default = "static/images/default_category.jpg")
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()

    
    
def category_scheme(category) -> dict:
    return {
        "id" : str(category["_id"]),
        "name" : category["name"],
        "image" : category["image"],
    }