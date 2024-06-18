from fastapi import APIRouter, Depends, Request, HTTPException
from fastapi.openapi.models import Response
from fastapi_cache.coder import JsonCoder
from sqlalchemy.orm import Session
from fastapi_cache.decorator import cache

from dependencies.db import get_db
from dependencies.user import get_current_user
from schemas.posts import PostCreate
from schemas.users import Token
from . import cruds

posts_router = APIRouter(
    prefix="/posts",
    tags=["posts"],
    responses={404: {"description": "Not found"}},
)


@posts_router.get("/")
@cache(expire=300)
async def get_user_posts(
        user: Token = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    return await cruds.get_user_posts(db=db, user_id=user.id)


@posts_router.post("/create-post")
async def create_post(
        content: PostCreate,
        user: Token = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    post = await cruds.create_post(db=db,
                                   content=content,
                                   user_id=user.id)
    return {"id": post.id}


@posts_router.delete("/delete-post/{post_id}")
async def delete_post(
        post_id: int,
        user: Token = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    if await cruds.delete_post(db=db, post_id=post_id, user_id=user.id):
        return {"message": f"Post {post_id} deleted successfully"}
    raise HTTPException(status_code=404, detail="Post not found")
