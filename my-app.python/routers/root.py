from fastapi import FastAPI, Depends, Header, Request, APIRouter
from pydantic import BaseModel
from google.cloud import firestore
import os
import uvicorn
import logging
import json
import time
import sys

routers = APIRouter()

logger = logging.getLogger(__name__)
handler = logging.StreamHandler(sys.stdout)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

class Response(BaseModel):
    message: str

@routers.get("/")
def _root():
    logger.info(f"get '/'")
    return Response(message="Hello, World")
