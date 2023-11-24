from bson import ObjectId
from fastapi import APIRouter, status, Depends
from typing import List

from passlib.context import CryptContext 
 
from db.client.db_config import db,users_collection,usersdb_collection
from db.models.user_model import *
from db.models import exeptions
from routers.jwt_auth_users import current_user



router = APIRouter(prefix="/user", tags=["user"], responses={status.HTTP_404_NOT_FOUND : {"message": "No encontrado"}})

crypt = CryptContext(schemes=["bcrypt"])

@router.get("/", response_model = List[User])
async def users(skip: int = 0, limit: int = 10, current_us: UserDB = Depends(current_user)):
    cursor = usersdb_collection.find().skip(skip).limit(limit)
    users = [User(**user_scheme(user)) async for user in cursor]
    return users



@router.get("/{id}", response_model= User)
async def user(id: str , current_us: UserDB = Depends(current_user)):
    try: 
        user = await usersdb_collection.find_one({"_id": ObjectId(id)})
        return User(**user_scheme(user))
    except:
        raise exeptions.USER_NOT_FOUND


@router.post("/" , response_model= User,status_code = status.HTTP_201_CREATED)
async def user_create(user: UserDB, current_us: UserDB = Depends(current_user)):
    
    if await users_collection.find_one({"username": user.username}):
        raise exeptions.USER_EXIST
    try:
        user.password = crypt.hash(user.password)
        userdb  = await usersdb_collection.insert_one(user.model_dump(by_alias=True, exclude={"id"}))
        user.id = str(userdb.inserted_id)
        
        return user
    
    except :
        await usersdb_collection.find_one_and_delete({"username": user.username})
        raise exeptions.USER_DONT_CREATE


@router.put("/{id}" , response_model= User , status_code= status.HTTP_200_OK)
async def user_update(id: str,user: UserDB, current_us: UserDB = Depends(current_user)):
    try:
        user.password = crypt.hash(user.password)
        user_dic = dict(user)
        del user_dic["id"]
        user = await usersdb_collection.find_one_and_replace({"_id": ObjectId(id)}, user_dic, return_document=True)
        return User(**user_scheme(user))
    except:
        raise exeptions.USER_NOT_FOUND

# Update user endpoint with PATCH
@router.patch("/{user_id}", response_model=User)
async def update_user(user_id: str, user_update: UpdateUser, current_us: UserDB = Depends(current_user)):
    
    existing_user = await usersdb_collection.find_one({"_id": ObjectId(user_id)})
    if existing_user:
        
        if user_update.password:
            user_update.password = crypt.hash(user_update.password)
        
        update_data = user_update.dict(exclude_unset=True)  # Exclude fields with None values
        updated_user = await usersdb_collection.find_one_and_update({"_id": ObjectId(user_id)}, {"$set": update_data}, return_document=True)
        
        return User(**user_scheme(updated_user))

    raise exeptions.USER_NOT_FOUND


@router.delete("/{id}" ,status_code = status.HTTP_204_NO_CONTENT)
async def user_delete(id: str , current_us: UserDB = Depends(current_user)):
    found  = await users_collection.find_one_and_delete({"_id": ObjectId(id)})
    
    if not found:
        raise exeptions.USER_NOT_FOUND
    