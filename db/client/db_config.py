from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import MongoClient
from typing import Optional


# Configuración de MongoDB
DATABASE_URL = "mongodb://localhost:27017"
#DATABASE_URL = "mongodb+srv://jorgeppr95106:951026jp@cluster0.jj3npoh.mongodb.net/?retryWrites=true&w=majority"
DB_NAME = "local"


# Configuración de MongoDB
client = AsyncIOMotorClient(DATABASE_URL)
db = client[DB_NAME]
users_collection = db["users"]
usersdb_collection = db["usersdb"]