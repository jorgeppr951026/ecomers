from lib2to3.pgen2.token import OP
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class Product(BaseModel):
    id: Optional[str] = None
    name: str
    price_buy: float
    proce_sell: float 
    image: Optional[str] = Field(default = "/static/images/new_product_logo.png")
    stock: int
    discount: Optional[float] = Field(default= 0)
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()
 
class UpdateProduct(BaseModel):
    name: Optional[str] = None
    price_buy: Optional[float] = None
    proce_sell: Optional[float] = None
    image: Optional[str] = None
    stock: Optional[int] = None
    discount: Optional[float] = None
 
    
    
def producto_scheme(producto) -> dict:
    return {
        "id" : str(producto["_id"]),
        "name" : producto["name"],
        "price_buy" : producto["price_buy"],
        "proce_sell" : producto["proce_sell"],
        "image" : producto["image"],
        "stock" : producto["stock"],
        "discount" : producto["discount"],
    }