import os
from fastapi import FastAPI
from routes import base, data
from motor.motor_asyncio import AsyncIOMotorClient
from helpers.config import get_settings
from contextlib import asynccontextmanager

MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
if not MONGODB_URI:
    raise ValueError("MONGODB_URI environment variable is not set.")

@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()
    mongo_conn = AsyncIOMotorClient(settings.MONGODB_URI)
    dp_client = mongo_conn[settings.mongo_db_name]

    app.state.mongo_conn = mongo_conn
    app.state.dp_client = dp_client

    print("MongoDB connected")

    yield

    mongo_conn.close()
    print("MongoDB disconnected")

app = FastAPI(lifespan=lifespan)

@app.get("/debug-db")
async def debug_db():
    collections = await app.state.dp_client.list_collection_names()
    return {
        "db_name": app.state.dp_client.name,
        "collections": collections
    }

# Include your routers
app.include_router(base.base_router)
app.include_router(data.data_router)




#@app.on_event("startup")
#async def startup_event():
#    settings = get_settings()
#    app.mongo_conn = AsyncIOMotorClient(MONGODB_URI)
#    app.dp_client = app.mongo_conn[settings.mongo_db_name]
#
#@app.on_event("shutdown")
#async def shutdown_event():
#    app.mongo_conn.close()

