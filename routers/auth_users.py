from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from jose import JWTError, jwt
from passlib.context import CryptContext
from bson import ObjectId
from datetime import datetime, timedelta

from db.client.db_config import users_collection

router = APIRouter()


# Configuración de seguridad para el token de acceso
SECRET_KEY = "09d25e094faa6ca1995c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


# Configuración de seguridad para el token de acceso
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")



# Modelo Pydantic para representar la información del usuario en la respuesta
class UserResponse(BaseModel):
    username: str
    email: str
    role: str



# Funciones de autenticación y autorización
def create_jwt_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt



async def get_current_user(token: str = Depends(oauth2_scheme)):
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

    user = await users_collection.find_one({"username": username})
    if user is None:
        raise credentials_exception
    return UserResponse(username=user["username"], email=user["email"], role=user["role"])



# Rutas para autenticación y autorización
@router.post("/token")
async def login_for_access_token(username: str, password: str):
    user = await users_collection.find_one({"username": username})
    if user and pwd_context.verify(password, user["password"]):
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_jwt_token(data={"sub": username}, expires_delta=access_token_expires)
        return {"access_token": access_token, "token_type": "bearer"}
    raise HTTPException(status_code=401, detail="Invalid credentials")



@router.post("/register")
async def register(username: str, email: str, password: str):
    hashed_password = pwd_context.hash(password)
    user = {"username": username, "email": email, "password": hashed_password, "role": "user"}
    result = await users_collection.insert_one(user)
    user["_id"] = result.inserted_id
    return user



@router.get("/users/me", response_model=UserResponse)
async def read_users_me(current_user: UserResponse = Depends(get_current_user)):
    return current_user
