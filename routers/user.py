from asyncio import exceptions
from bson import ObjectId
from fastapi import APIRouter, status , HTTPException
from jose import JWSError
from typing import List, Sized

from db.client.db_config import db,users_collection,usersdb_collection
from db.models.user import User, UserDB, user_scheme

from db.models import exeptions

router = APIRouter(prefix="/user", tags=["user"], responses={status.HTTP_404_NOT_FOUND : {"message": "No encontrado"}})


@router.get("/", response_model = List[User])
async def users(skip: int = 0, limit: int = 10):
    cursor = users_collection.find().skip(skip).limit(limit)
    users = [User(**user_scheme(user)) async for user in cursor]
    return users



@router.get("/{id}", response_model= User)
async def user(id: str):
    try: 
        user = await users_collection.find_one({"_id": ObjectId(id)})
        return User(**user_scheme(user))
    except:
        raise exeptions.USER_NOT_FOUND


@router.post("/" , response_model= User,status_code = status.HTTP_201_CREATED)
async def user_create(user: User):
    
    if await users_collection.find_one({"username": user.username}):
        raise exeptions.USER_EXIST
    try:
        new_user = await users_collection.insert_one(user.model_dump(by_alias=True, exclude={"id"}))
        user.id = str(new_user.inserted_id)
        return user
    
    except :
        raise exeptions.USER_DONT_CREATE

@router.put("/" , response_model= User , status_code= status.HTTP_200_OK)
async def user_update(user: User):
    try:
        user_dic = dict(user)
        del user_dic['id']
        
        user = await users_collection.find_one_and_replace({"_id": ObjectId(user.id)}, user_dic, return_document=True)
        return User(**user_scheme(user))
    except:
        raise exeptions.USER_NOT_FOUND


@router.delete("/{id}" ,status_code = status.HTTP_204_NO_CONTENT)
async def user_delete(id: str):
    found  = await users_collection.find_one_and_delete({"_id": ObjectId(id)})
    
    if not found:
        raise exeptions.USER_NOT_FOUND
    