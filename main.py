from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from routers import  user,jwt_auth_users,category, type

app = FastAPI()

#Routers
app.include_router(user.router)
app.include_router(jwt_auth_users.router)
app.include_router(category.router)
app.include_router(type.router)


#Static Files
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
async def index():
    return {
        'index': 'http://127.0.0.1:8000',
        'swager': 'http://127.0.0.1:8000/docs'
    }
    
    

#Run server localhost -> uvicorn main:app --reload
#Url localhost -> http://127.0.0.1:8000
#Swagger Docs -> http://127.0.0.1:8000/docs