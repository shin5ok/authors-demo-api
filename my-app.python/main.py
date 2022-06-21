from fastapi import FastAPI, Depends, Header, Request
from pydantic import BaseModel
from google.cloud import firestore
import os
import uvicorn
import logging
import json
import time
import sys

COLLECTION: str = "authors"

app = FastAPI()
db = firestore.Client()

logger = logging.getLogger(__name__)
handler = logging.StreamHandler(sys.stdout)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)
class Response(BaseModel):
    message: str

class Author(BaseModel):
    mail: str
    username: str
    name: str
    address: str
    company: str
    job: str
    website: list

class AuthorResponse(BaseModel):
    data: Author

@app.get("/")
def _root():
    logger.info(f"get '/'")
    return Response(message="Hello, World")

@app.get("/api/author/{username}")
def _author_get(username: str, request: Request, user_agent = Header(default=None), host = Header(default=None), ):

    start_time = time.time()

    docs = db.collection(COLLECTION).where("username", "==", username).limit(1)
    result = docs.stream()
    data = list(result)[-1]
    response_data = data.to_dict()

    process_time = time.time() - start_time

    logger.info(json.dumps(dict(path=f"/api/author/{username}", user_agent=user_agent, host=host, process_time=process_time, remote_addr=request.client.host)))
    return AuthorResponse(data=response_data)

if __name__ == '__main__':
    port = os.environ.get("PORT", "8080")
    options = {
            'port': int(port),
            'host': '0.0.0.0',
            'workers': 2,
            'reload': True,
        }
    uvicorn.run("main:app", **options)