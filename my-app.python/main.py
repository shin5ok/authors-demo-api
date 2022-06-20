from fastapi import FastAPI, Depends
from pydantic import BaseModel
from google.cloud import firestore

COLLECTION: str = "authors"

app = FastAPI()

db = firestore.Client()

class Response(BaseModel):
    message: str

class AuthorResponse(BaseModel):
    data: dict

@app.get("/")
def _root():
    return Response(message="Hello, World")

@app.get("/api/author/{username}")
def _author_get(username: str):
    docs = db.collection(COLLECTION).where("username", "==", username).limit(1)
    result = docs.stream()
    data = list(result)[-1]
    return AuthorResponse(data=data.to_dict())