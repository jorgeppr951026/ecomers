from dataclasses import Field
from typing import Optional
from pydantic import BaseModel,Field, EmailStr
from bson import ObjectId




class User(BaseModel):
    id: Optional[str] = Field(alias="id", default=None) 
    username: str
    email: str
    disable: bool

    class Config:
        json_encoders = {ObjectId: str}
        

class UserDB(User):
    password: str
    
class UpdateUser(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    disable: Optional[bool] = None
    password: Optional[str] = None
    

def user_scheme(user) -> dict:
   
    return {
        "id" : str(user["_id"]),
        "username" : user["username"],
        "email" : user["email"],
        "disable" : user["disable"],
    } 

def userdb_scheme(user) -> dict:
    return {
        "id" : str(user["_id"]),
        "username" : user["username"],
        "email" : user["email"],
        "disable" : user["disable"],
        "password" : user["password"],
    }