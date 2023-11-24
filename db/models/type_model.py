from pydantic import BaseModel, Field
from bson import ObjectId
from typing import Optional


class Type(BaseModel):
    id: Optional[str] = Field(default=None)
    type: str

    
    
def type_scheme(type) -> dict:
    return {
        "id" : str(type["_id"]),
        "type" : type["type"],
    }