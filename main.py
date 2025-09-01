from typing import List, Optional
from fastapi import FastAPI, Response
from pydantic import BaseModel
from starlette import status
from starlette.responses import HTMLResponse

app = FastAPI(title="Blog API", version="1.0")

class PostCreate(BaseModel):
    author: str
    title: str
    content: str

class Post(PostCreate):
    id: int


posts_db: List[Post] = [
    Post(id=1, author="Lucas Clavel", title="Les temps d'automne", content="Livre long")
]

# Q1
@app.get("/ping", response_class=Response)
def read_ping():
    return Response(content="Pong", status_code=status.HTTP_200_OK, media_type="text/plain")


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


# Q4 - Créer un ou plusieurs posts
@app.post("/posts", response_model=List[Post], status_code=status.HTTP_201_CREATED)
def create_posts(new_posts: List[PostCreate]):
    start_id = len(posts_db) + 1
    created_posts = [
        Post(id=start_id + i, **post.dict()) for i, post in enumerate(new_posts)
    ]
    posts_db.extend(created_posts)
    return created_posts


# Q5 - Récupérer tous les posts
@app.get("/posts", response_model=List[Post], status_code=status.HTTP_200_OK)
def get_posts():
    return posts_db


# Q6 - Mettre à jour un post par ID
@app.put("/posts/{post_id}", response_model=Post, status_code=status.HTTP_200_OK)
def update_post(post_id: int, new_post: PostCreate):
    for i, existing_post in enumerate(posts_db):
        if existing_post.id == post_id:
            updated_post = Post(id=post_id, **new_post.model_dump())
            posts_db[i] = updated_post
            return updated_post

    # Si le post n'existe pas encore, on l'ajoute
    new_post_with_id = Post(id=post_id, **new_post.model_dump())
    posts_db.append(new_post_with_id)
    return new_post_with_id
