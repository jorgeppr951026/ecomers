from operator import ne
from bson import ObjectId
from fastapi import APIRouter, status
from typing import List



from db.models.producto_model import Product, UpdateProduct, producto_scheme
from db.models.exeptions import raise_exept
from db.client.db_config import product_collection

router = APIRouter(prefix="/products", tags=["products"], responses={status.HTTP_404_NOT_FOUND : {"message": "No encontrado"}})


@router.get("/", response_model=List[Product])
async def get_products(skip: int = 0, limit: int = 10, type_id = None):
    cursor = []
   
    if type_id:
        cursor = product_collection.find({"type_id": ObjectId(type_id)}).skip(skip).limit(limit)
    else:
        cursor =  product_collection.find().skip(skip).limit(limit)
        
    products_list = [Product(**producto_scheme(product)) async for product in cursor]
    return products_list
    

@router.get("/{id}", response_model=Product)
async def get_product(id: str):
    product = await product_collection.find_one({"_id": ObjectId(id)})
    if product:
        return  producto_scheme(product)
    raise raise_exept(status.HTTP_400_BAD_REQUEST, "No se a encontrado el producto")


@router.delete("/{id}" , status_code= status.HTTP_204_NO_CONTENT)
async def delete_product(id: str):
    product = await product_collection.find_one_and_delete({"_id": ObjectId(id)})
    if not product:
        raise raise_exept(status.HTTP_400_BAD_REQUEST, "No se a encontrado el producto")


@router.post("/{type_id}", response_model=Product , status_code= status.HTTP_201_CREATED)
async def create_product(product: Product, type_id: str):
    found  = await product_collection.find_one({"name": product.name})
    if not type_id:
        raise_exept(status.HTTP_400_BAD_REQUEST, "Debe enviar el tipo de producto")
    
    if not found:
        try:
            product_dict = product.model_dump(exclude={"id"})
            product_dict["type_id"] = ObjectId(type_id)
            new_product = await product_collection.insert_one(product_dict) 
            product.id = str(new_product.inserted_id)
            return product
        except:
            raise raise_exept(status.HTTP_400_BAD_REQUEST, "No se pudo crear el producto")
        
    raise raise_exept(status.HTTP_400_BAD_REQUEST, "Ya esxiste un producto con ese nombre")



@router.patch("/{id}", response_model=Product)
async def update_product(id: str, product_update: UpdateProduct):
    
    existing_product = await product_collection.find_one({"_id": ObjectId(id)})
    if existing_product:
        update_data =  product_update.model_dump(exclude_unset=True)  # Exclude fields with None values
        updated_product = await product_collection.find_one_and_update({"_id": ObjectId(id)}, {"$set": update_data}, return_document=True)
        
        return Product(**producto_scheme(updated_product))

    raise raise_exept(status.HTTP_400_BAD_REQUEST, "El producto que desea actualizar no existe")
        
