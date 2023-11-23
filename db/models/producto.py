from pydantic import BaseModel


class Producto(BaseModel):
    name: str
    price_buy: float
    proce_sell: float 
    image: str | str("/static/images/new_product_logo.png")
    
    
    
def producto_scheme(producto) -> dict:
    return {
        "id" : str(producto["_id"]),
        "name" : producto["name"],
        "price_buy" : producto["price_buy"],
        "proce_sell" : producto["proce_sell"],
        "image" : producto["image"],
    }