from fastapi import FastAPI
from routes import base, data,nlp
from motor.motor_asyncio import AsyncIOMotorClient
from helpers.config import get_settings
from contextlib import asynccontextmanager
from stores.llm.LLMProviderFactory import LLMProviderFactory
from stores.VectorDB.VectorProviderFactory import VectorProviderFactory
import logging

logger = logging.getLogger(__name__)



@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()
    mongo_conn = AsyncIOMotorClient(settings.MONGODB_URI)
    dp_client = mongo_conn[settings.mongo_db_name]

    app.state.mongo_conn = mongo_conn
    app.state.dp_client = dp_client


    print("MongoDB connected")

    llmProviderFactory = LLMProviderFactory(settings)
    vector_provider_factory = VectorProviderFactory(settings)

    #generation_client
    app.state.generation_client = llmProviderFactory.create(provider=settings.generation_groq_backend)
    app.state.generation_client.set_generation_model(model_name=settings.Generation_model_id)
    #embedding_client
    app.state.embedding_client = llmProviderFactory.create(provider=settings.Embedding_backend)
    app.state.embedding_client.set_embedings_model(model_name=settings.Embedding_model_id,embeding_size = settings.Embedding_model_size)
    #vector_client 
    app.state.vectordb_client = vector_provider_factory.create(provider_name=settings.vector_db_backend)
    app.state.vectordb_client.connect()

    yield

    mongo_conn.close()
    logger.info("MongoDB disconnected")
    app.state.vectordb_client.disconnect()
    

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
app.include_router(nlp.nlp_router)




