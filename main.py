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


# EXO1 - b
@app.post("/phones", response_model=List[Phone], status_code=status.HTTP_201_CREATED)
def create_phones(new_phone: List[Phone]):
    start_id = len(phones_db) + 1
    created_phone = [
        Post(id=start_id + i, **post.dict()) for i, post in enumerate(new_phone)
    ]
    phones_db.extend(created_phone)
    return created_phone


# Q5 - Récupérer tous les posts
@app.get("/posts", response_model=List[Post], status_code=status.HTTP_200_OK)
def get_posts():
    return phones_db


# Q6 - Mettre à jour un post par ID
@app.put("/posts/{post_id}", response_model=Post, status_code=status.HTTP_200_OK)
def update_post(post_id: int, new_post: Phone):
    for i, existing_post in enumerate(phones_db):
        if existing_post.id == post_id:
            updated_post = Post(id=post_id, **new_post.model_dump())
            phones_db[i] = updated_post
            return updated_post

    # Si le post n'existe pas encore, on l'ajoute
    new_post_with_id = Post(id=post_id, **new_post.model_dump())
    phones_db.append(new_post_with_id)
    return new_post_with_id
