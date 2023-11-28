from fastapi import APIRouter, Body, status, Depends, File, UploadFile, Form
from fastapi.encoders import jsonable_encoder
from bson import ObjectId
from PIL import Image
from typing import List

from db.client.db_config import category_collection, type_collection, product_collection
from db.models.category_model import Category,category_scheme
from db.models.type_model import Type, type_scheme
from db.models.exeptions import raise_exept

import uuid, os

router = APIRouter(prefix="/categorys", tags=["category"], responses={status.HTTP_404_NOT_FOUND : {"message": "No encontrado"}})




@router.get("/",response_model=List[Category])
async def categorys(skip: int = 0, limit: int = 10):
    cursor = category_collection.find().skip(skip).limit(limit)
    categorys = [Category(**category_scheme(category)) async for category in cursor]
    return categorys


@router.get("/{id}",response_model=Category)
async def category(id: str):
    category = await category_collection.find_one({"_id": ObjectId(id)})
    
    return category_scheme(category)


@router.get("/{id}/count", response_model=dict)
async def category_count(id: str):
    types = type_collection.find({"category_id": ObjectId(id)})
    types = await types.to_list(length=None)
    count = 0
    for val in types:
       count += await product_collection.count_documents({"type_id": val['_id']})
    return {"count_types": len(types), "count_products": count}



@router.post("/", response_model= Category, status_code= status.HTTP_201_CREATED )
async def category_create(category: Category):
    if await category_collection.find_one({"name": category.name}):
        raise raise_exept(status.HTTP_400_BAD_REQUEST, "Esa categoria ya existe")
    try:
      
        cate = await category_collection.insert_one(jsonable_encoder(category))
        new_cate = await category_collection.find_one({"_id": cate.inserted_id})
      
        return category_scheme(new_cate)
    except :
        raise raise_exept(status.HTTP_400_BAD_REQUEST, "No se pudo crear la categoria")

@router.post("/{id}/upload/")
async def create_upload_file(id: str ,file: UploadFile = File(...)):
    # Generar un nombre único para el archivo
    item = category_scheme(await category_collection.find_one({"_id": ObjectId(id)}))
    if not "default" in item['image']:
        eliminar_imagen_anterior(item['image'])
        
    random_token = str(uuid.uuid4())
    extension = str(file.filename).split(".")[-1]
    image_path = f"static/images/{random_token}.{extension}"
    file_content = await file.read()
    
    with open(image_path, "wb") as image_file:
        image_file.write(file_content)
        
    with Image.open(image_path) as image:
        image = image.resize(size= (400,400))
        image.save(image_path)
        
    image_file.close()
    image.close()
    
    updated_categorie = await category_collection.update_one({"_id": ObjectId(id)}, {"$set": {"image": image_path}})
   
    return {"message": "La imagense actualizo satisfactoriamente"}


@router.put("/{id}" , response_model= Category )
async def category_update(id: str, category: Category):
    try:
        category_dic = dict(category)
        del category_dic["id"]
        new_category = await category_collection.find_one_and_replace({"_id": ObjectId(id)}, category_dic, return_document=True)
        return category_scheme(new_category)
    except:
        raise raise_exept(status.HTTP_404_NOT_FOUND,"No se ha encontrado la categoria")
    

@router.delete("/{id}" ,status_code = status.HTTP_204_NO_CONTENT)
async def category_delete(id: str ):
    found  = await category_collection.find_one_and_delete({"_id": ObjectId(id)})
    
    if not found:
        raise raise_exept(status.HTTP_404_NOT_FOUND,"No se ha encontrado la categoria")
    
    
    
def eliminar_imagen_anterior(ruta_imagen_anterior):
  
    if os.path.exists(ruta_imagen_anterior):
        try:
            # Elimina la imagen
            os.remove(ruta_imagen_anterior)
        except Exception as e:
            print(f"No se pudo eliminar la imagen. Error: {e}")
    else:
        print(f"La imagen {ruta_imagen_anterior} no existe.")