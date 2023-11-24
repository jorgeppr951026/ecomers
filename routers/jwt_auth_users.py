from fastapi import APIRouter, FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel

from jose import jwt, JWTError
from passlib.context import CryptContext

from datetime import datetime, timedelta
from typing import Optional

from db.client.db_config import usersdb_collection
from db.models.user_model import User, UserDB, userdb_scheme, user_scheme
from db.models import exeptions

SECRET_KEY = "09d25e094faa6ca1995c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


crypt = CryptContext(schemes=["bcrypt"])

router = APIRouter()
oauth2 = OAuth2PasswordBearer(tokenUrl="login")



def create_access_token(data: dict, expires_delta: timedelta ):
 
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt




async def serarch_user_db(username: str) -> UserDB:
    userdb = await usersdb_collection.find_one({"username": username})
    
    if userdb is None:
        raise exeptions.USER_DONT_EXIST
    return UserDB(**userdb_scheme(userdb))


async def auth_user(token: str = Depends(oauth2)):
    try:
        username = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM]).get("sub")
        if username is None:
            raise exeptions.INVALID_CREDENTIALS
    except JWTError:
        raise exeptions.INVALID_CREDENTIALS

    return await serarch_user_db(username)


async def current_user(user: UserDB = Depends(auth_user)) -> User:
    if user.disable:
        raise exeptions.USER_INACTIVE
    return user


@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user = await serarch_user_db(form.username)
    if not user:
        raise exeptions.WRONG_USER

    if not crypt.verify(form.password, user.password): # type: ignore
        raise exeptions.WRONG_PASSW

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username, }, # type: ignore
        expires_delta=access_token_expires,
    )

    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/users/me")
async def me(user: UserDB = Depends(current_user)) :
    user_dict = user.dict()
    del user_dict["password"]
    return user_dict