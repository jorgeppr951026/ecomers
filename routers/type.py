from unicodedata import category
from bson import ObjectId
from fastapi import APIRouter, status, Depends
from typing import List

from passlib.context import CryptContext 
 
from db.client.db_config import type_collection, category_collection
from db.models.type_model import Type,type_scheme
from db.models.exeptions import raise_exept
from routers.jwt_auth_users import current_user



router = APIRouter(prefix="/types", tags=["types"], responses={status.HTTP_404_NOT_FOUND : {"message": "No encontrado"}})


@router.get("/",response_model=List[Type])
async def types(skip: int = 0, limit: int = 10):
    cursor = type_collection.find().skip(skip).limit(limit)
    types = [Type(**type_scheme(type)) async for type in cursor]
    return types

@router.get("/{id}",response_model=Type)
async def type(id: str):
    type = await type_collection.find_one({"_id": ObjectId(id)})
    return type_scheme(type)


@router.put("/{id}" , response_model= Type )
async def type_update(id: str, type: Type):
    try:
        type_dic = dict(type)
        del type_dic["id"]
        new_type = await type_collection.find_one_and_replace({"_id": ObjectId(id)}, type_dic, return_document=True)
        return type_scheme(new_type)
    except:
        raise raise_exept(status.HTTP_404_NOT_FOUND,"No se ha encontrado la categoria")
    

@router.delete("/{id}" ,status_code = status.HTTP_204_NO_CONTENT)
async def type_delete(id: str ):
    found  = await type_collection.find_one_and_delete({"_id": ObjectId(id)})
    
    if not found:
        raise raise_exept(status.HTTP_404_NOT_FOUND,"No se ha encontrado la categoria")