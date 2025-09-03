from typing import List, Optional
from fastapi import FastAPI, Response
from pydantic import BaseModel
from starlette import status
from starlette.responses import HTMLResponse

# lancer le server : uvicorn main:app --reload
app = FastAPI(title="Blog API", version="1.0")

class Phone(BaseModel):
    identifier: str
    brand: str
    model: str
    characteristics: str

class Post(Phone):
    id: int


phones_db: List[Phone] = [
    Phone(identifier="1", brand="Samsung", model="A22", characteristics="robuste")
]

# EXO1 - a
@app.get("/health", response_class=Response)
def read_health():
    return Response(content="Ok", status_code=status.HTTP_200_OK, media_type="text/plain")


# EXO1 - b
@app.post("/phones", response_model=List[Phone], status_code=status.HTTP_201_CREATED)
def create_phones(new_phone: List[Phone]):
    start_id = len(phones_db) + 1
    created_phone = [
        Post(id=start_id + i, **post.dict()) for i, post in enumerate(new_phone)
    ]
    phones_db.extend(created_phone)
    return created_phone

# EXO1 - c
@app.get("/posts", response_model=List[Phone], status_code=status.HTTP_200_OK)
def get_phones():
    return phones_db

# EXO1 - d
@app.get("/phones/{phone_id}", response_model=Post, status_code=status.HTTP_200_OK)
def read_phone_by_id(phone_id: int):
    for i, existing_post in enumerate(phones_db):
        if existing_post.id == phone_id:
            return existing_post
        else:
            return Response(status_code=status.HTTP_404_NOT_FOUND)

# Q2
@app.get("/home", response_class=HTMLResponse, status_code=status.HTTP_200_OK)
def welcome_home():
    return """
        <!doctype html>
            <html lang="en">
            <head>
                <meta charset="UTF-8" />
                <title>Accueil</title>
            </head>
            <body>
                <h1>Welcome home!</h1>
            </body>
        </html>
    """


