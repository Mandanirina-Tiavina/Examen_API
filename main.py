from typing import List
from fastapi import FastAPI
from pydantic import BaseModel
from starlette.responses import Response, JSONResponse

app = FastAPI()

# Model for Player
class posts(BaseModel):
    author: str
    title: str
    content: str
    creation_datetime: str


# In-memory store for players
published: List[posts] = []

# Serialize players to JSON-compatible format
def serialized_posts():
    posts_converted = []
    for posts in published:
        posts_converted.append(posts.model_dump())
    return posts_converted

@app.get("/ping")
def hello():
        return Response(content="pong", status_code=200)

@app.get("/home")
def welcome():
    with open("home.html", "r", encoding="utf-8") as file:
        html_content = file.read()
    return Response(content=html_content, status_code=200, media_type="text/html")

@app.post("/posts")
def new_posts(posts_published: List[posts]):
    published.extend(posts_published)
    return Response(content={"posts": serialized_posts()}, status_code=201)

@app.get("/posts")
def list_posts():
    return JSONResponse(content={"players": serialized_posts()}, status_code=200)

@app.put("/posts")
def update_or_create_posts(posts_published: List[posts]):
    global published
    for new_posts in posts_published:
        found = False
        for i, existing_posts in enumerate(published):
            if new_posts.title == existing_posts.title:
                published[i] = new_posts
                found = True
                break
        if not found:
            published.append(new_posts)
    return JSONResponse(content={"posts": serialized_posts()}, status_code=200)

@app.get("/{full_path:path}")
def catch_all(full_path: str):
        with open("not_found.html", "r", encoding="utf-8") as file:
            html_content = file.read()
        return Response(content=html_content, status_code=404, media_type="text/html")