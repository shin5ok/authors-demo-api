from fastapi import FastAPI, Depends, Header, Request, APIRouter
from pydantic import BaseModel, Field, EmailStr
from google.cloud import firestore
import os
import uvicorn
import logging
import json
import time
import sys

COLLECTION: str = os.environ.get("COLLECTION", "authors")
db = firestore.Client()

def get_coll():
    docs = db.collection(COLLECTION)
    return docs