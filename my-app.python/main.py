from fastapi import FastAPI, Depends
from pydantic import BaseModel
from google.cloud import firestore
import os
import uvicorn
import logging

COLLECTION: str = "authors"

app = FastAPI()
db = firestore.Client()

logger = logging.getLogger('uvicorn')

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
def _author_get(username: str):
    docs = db.collection(COLLECTION).where("username", "==", username).limit(1)
    result = docs.stream()
    data = list(result)[-1]
    logger.info(f"get '{username}'")
    return AuthorResponse(data=data.to_dict())

if __name__ == '__main__':
    port = os.environ.get("PORT", "8080")
    options = {
            'port': int(port),
            'host': '0.0.0.0',
            'workers': 2,
        }
    uvicorn.run("main:app", **options)