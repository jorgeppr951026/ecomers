from fastapi import APIRouter, FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel

from jose import jwt, JWTError
from passlib.context import CryptContext

from datetime import datetime, timedelta

from db.client.db_config import users_collection,usersdb_collection
from db.models.user import User, UserDB

SECRET_KEY = "09d25e094faa6ca1995c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1


crypt = CryptContext(schemes=["bcrypt"])

router = APIRouter()
oauth2 = OAuth2PasswordBearer(tokenUrl="login")



def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def serarch_user(username: str):
    user = await users_collection.find_one({"username": username})
    if user is None:
        raise HTTPException(status_code= status.HTTP_401_UNAUTHORIZED,
                            detail="El usuario no existe",
                            headers={"WWW-Authenticate": "Bearer"},)
    return User(**user)

async def serarch_user_db(username: str):
    userdb = await usersdb_collection.find_one({"username": username})
    if userdb is None:
        raise HTTPException(status_code= status.HTTP_401_UNAUTHORIZED,
                            detail="El usuario no existe",
                            headers={"WWW-Authenticate": "Bearer"},)
    return UserDB(**userdb[username])


async def auth_user(token: str = Depends(oauth2)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        username = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM]).get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    return serarch_user(username)


async def current_user(user: User = Depends(auth_user)) -> User:
    if user.disable:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Usuario inactivo")
    return user


@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user = user_db.get(form.username)
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="El usuario no es correcto.")

    user = serarch_user_db(form.username)

    if not crypt.verify(form.password, user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="La contraseña no es correcta.")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username, },
        expires_delta=access_token_expires,
    )

    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/users/me")
async def me(user: User = Depends(current_user)) -> User:
    return user
