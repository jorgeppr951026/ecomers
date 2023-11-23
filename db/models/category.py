from pydantic import BaseModel




class Category(BaseModel):
    id: str | None
    name: str
    type: str
    
    
def category_scheme(category) -> dict:
    return {
        "id" : str(category["_id"]),
        "name" : category["name"],
        "type" : category["type"],
    }