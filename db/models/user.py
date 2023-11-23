from dataclasses import Field
from typing import Optional
from pydantic import BaseModel,Field, ConfigDict
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
    
    

def user_scheme(user) -> dict:
   
    return {
        "id" : str(user["_id"]),
        "username" : user["username"],
        "email" : user["email"],
        "disable" : user["disable"],
    }   