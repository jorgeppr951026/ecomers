from bson import ObjectId
from fastapi import APIRouter, status, Depends
from typing import List

from passlib.context import CryptContext 
 
from db.client.db_config import category_collection, type_collection
from db.models.category_model import Category,category_scheme
from db.models.type_model import Type, type_scheme
from db.models.exeptions import raise_exept
from routers.jwt_auth_users import current_user



router = APIRouter(prefix="/categorys", tags=["category"], responses={status.HTTP_404_NOT_FOUND : {"message": "No encontrado"}})


@router.get("/",response_model=List[Category])
async def categorys(skip: int = 0, limit: int = 10):
    cursor = category_collection.find().skip(skip).limit(limit)
    categorys = [Category(**category_scheme(category)) async for category in cursor]
    return categorys


@router.get("/types",response_model=List[Category])
async def categorys_whit_cosmetics(skip: int = 0, limit: int = 10):
    
    #categorys = [Category(**category_scheme(category)) async for category in cursor]
    #return categorys
    pass


@router.get("/{id}",response_model=Category)
async def category(id: str):
    category = await category_collection.find_one({"_id": ObjectId(id)})
    return category_scheme(category)


@router.post("/", response_model= Category, status_code= status.HTTP_201_CREATED)
async def category_create(category: Category):
    if await category_collection.find_one({"name": category.name}):
        raise raise_exept(status.HTTP_400_BAD_REQUEST, "Esa categoria ya existe")
    try:
        cate = await category_collection.insert_one(category.model_dump())
        new_cate = await category_collection.find_one({"_id": cate.inserted_id})
        return category_scheme(new_cate)
    except :
        raise raise_exept(status.HTTP_400_BAD_REQUEST, "No se pudo crear la categoria")



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
    
    
    
#Create type
@router.post("/{category_id}/type", response_model= Type, status_code= status.HTTP_201_CREATED)
async def type_create(category_id:str, type: Type):
    category = await category_collection.find_one({"_id": ObjectId(category_id)})
    
    if category:
        
        if await type_collection.find_one({"type": type.type}):
            raise raise_exept(status.HTTP_400_BAD_REQUEST, f"Ese tipo de {category['name']} ya existe")
        
        try:
            type_dict = type.dict()
            type_dict['category_id'] = ObjectId(category_id)
            type_in_db = await type_collection.insert_one(type_dict)
            type.id = str(type_in_db.inserted_id)
            return type
        except :
            raise raise_exept(status.HTTP_400_BAD_REQUEST, "No se pudo crear el tipo")
    raise raise_exept(status.HTTP_400_BAD_REQUEST, f"Esa categoria no existe")