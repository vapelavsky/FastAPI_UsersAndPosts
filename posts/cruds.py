from sqlalchemy.orm import Session

from db.models import Post
from schemas.posts import PostCreate


async def get_user_posts(db: Session, user_id: int):
    return db.query(Post).filter(Post.user_id == user_id).all()


async def create_post(db: Session,
                      user_id: int,
                      content: PostCreate):
    new_post = Post(user_id=user_id,
                    content=content.content)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


async def delete_post(db: Session, post_id: int, user_id: int):
    post = db.query(Post).filter(Post.id == post_id).first()
    if post.user_id == user_id:
        db.delete(post)
        db.commit()
        return True
    return False
