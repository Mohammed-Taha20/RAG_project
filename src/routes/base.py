from asyncio import base_events
import re
from fastapi import FastAPI, APIRouter,Depends
import os
from helpers.config import get_settings


base_router = APIRouter(prefix= "/api/v1" , tags=["api_v1"])

@base_router.get("/")
async def root():
    app_settings = get_settings()
    app_name = app_settings.APP_name
    app_version = app_settings.APP_version
    app_discribtion = app_settings.APP_description
    app_id = app_settings.APP_ID
    app_author = app_settings.APP_author
    return {"app_name": app_name,
            "app_version": app_version,
            "app_discribtion": app_discribtion,
            "app_id": app_id,
            "app_author": app_author
            }
