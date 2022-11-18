from fastapi import FastAPI, Depends, Header, Request, APIRouter
from pydantic import BaseModel, Field, EmailStr
from google.cloud import firestore
import os
import uvicorn
import logging
import json
import time
import sys

from common import get_coll

app = FastAPI()
db = firestore.Client()

routers = APIRouter()

logger = logging.getLogger(__name__)
handler = logging.StreamHandler(sys.stdout)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

class Response(BaseModel):
    message: str

class Author(BaseModel):
    mail: None | EmailStr
    username: str = Field(min=2, max=32, regex="[0-9a-z\-]+")
    name: str
    address: str
    company: str
    job: str
    website: list

class AuthorResponse(BaseModel):
    data: Author

@routers.get("/author/{username}")
def _author_get(username: str, request: Request, user_agent = Header(default=None), host = Header(default=None), s = Depends(get_coll)):

    start_time = time.time()

    docs = s.document(username)
    response_data = docs.get()

    process_time = time.time() - start_time

    logger.info(json.dumps(dict(path=f"/api/author/{username}", method=request.method, user_agent=user_agent, host=host, process_time=process_time, remote_addr=request.client.host)))
    return AuthorResponse(data=response_data.to_dict())

@routers.post("/author/{username}")
def _author_post(author: Author, username: str, request: Request, user_agent = Header(default=None), host = Header(default=None), s = Depends(get_coll)):

    start_time = time.time()

    docs = s.document(username)
    docs.set(author.dict())

    process_time = time.time() - start_time

    logger.info(json.dumps(dict(path=f"/api/author/{username}", method=request.method, user_agent=user_agent, host=host, process_time=process_time, remote_addr=request.client.host)))
    return AuthorResponse(data=author)


@routers.put("/author/{username}")
def _author_put(author: Author, username: str, request: Request, user_agent = Header(default=None), host = Header(default=None), s = Depends(get_coll)):

    start_time = time.time()

    docs = s.document(username)
    docs.set(author.dict())

    process_time = time.time() - start_time

    logger.info(json.dumps(dict(path=f"/api/author/{username}", method=request.method, user_agent=user_agent, host=host, process_time=process_time, remote_addr=request.client.host)))
    return AuthorResponse(data=author)
