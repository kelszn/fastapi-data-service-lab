from typing import Optional
from random import randrange

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel


class PostCreate(BaseModel):
    # id removed — server-authored, never client-writable
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None
    


app = FastAPI()





my_posts = [
    {"id": 1, "title": "music", "content": "music is art!",
     "published": False, "rating": 9},
    {"id": 2, "title": "football", "content": "football is amazing!",
     "published": True, "rating": 5},
]


def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p
    return None




def find_post_index(id):
    for i, p in enumerate(my_posts):
        if p["id"] == id:
            return i          # the index, not the post
    return None






@app.get("/")
def root():
    return {"message": "Hello World"}







@app.get("/posts")
def get_posts():
    return {"My Posts": my_posts}








@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: PostCreate):
    post_dict = post.model_dump()
    post_dict["id"] = randrange(5, 1_000_000)   # per request, not per import
    my_posts.append(post_dict)
    return {"Created Post": post_dict}








@app.get("/posts/latest")
def get_latest_post():
    if not my_posts:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="there are no posts yet",
        )
    return {"Latest Post": my_posts[-1]}









@app.get("/posts/{id}")
def get_post(id: int):
    post = find_post(id)
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id no:{id} was not found",
        )
    return {"Selected Post": post}






@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    index = find_post_index(id)
    if index is None:                 # NOT `if not index` — see below
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id no:{id} was not found",
        )
    my_posts.pop(index)
    return status.HTTP_204_NO_CONTENT
    # 204 means no content — return nothing at all






@app.put("/posts/{id}", status_code=status.HTTP_200_OK)
def update_post(id: int, post: PostCreate):
    index = find_post_index(id)
    if index is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id no:{id} was not found",
        )

    post_dict = post.model_dump()   # PostCreate object -> plain dict
    post_dict["id"] = id            # preserve the id from the URL
    my_posts[index] = post_dict     # replace in place, no pop + insert

    return f'Updated Post": {post_dict}'
