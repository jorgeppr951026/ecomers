from fastapi import APIRouter, FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel


app = FastAPI()

oauth2 = OAuth2PasswordBearer(tokenUrl="login")


class User(BaseModel):
    username: str
    full_name: str
    email: str
    disable: bool


class UserDB(User):
    password: str


user_db = {
    "jorge": {
        "username": "jorge",
        "full_name": "Jorge Pastor",
        "email": "jorge@gamil.com",
        "disable": False,
        "password": "12345678"
    },
    "jorge2": {
        "username": "jorge2",
        "full_name": "Jorge Pastor",
        "email": "jorge2@gamil.com",
        "disable": True,
        "password": "12345678"
    }
}

def serarch_user_db(username: str) -> UserDB:
    if username in user_db:
        return UserDB(**user_db[username])
    
def serarch_user(username: str) -> User:
    if username in user_db:
        return User(**user_db[username])


async def current_user(token: str = Depends(oauth2)) -> UserDB:
    user = serarch_user(token)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Credenciales de autenticación inválidas",
                            headers={"WWW-Authenticate": "bearer"})
    if user.disable:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Usuario inactivo")
    return user


@app.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user = user_db.get(form.username)
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="El usuario no es correcto.")

    user = serarch_user_db(form.username)

    if not form.password == user.password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="La contraseña no es correcta.")

    return {"access_token": f"{user.username}", "token_type": "bearer"}


@app.get("/users/me")
async def me(user: User = Depends(current_user)) -> User:
    return user
