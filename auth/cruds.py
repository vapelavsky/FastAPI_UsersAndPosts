from sqlalchemy.orm import Session

from auth.helpers import hash_password, verify_password, create_access_token
from schemas.users import UserCreate
from db.models import User


async def create_user(db: Session, user: UserCreate):
    db_user = User(email=user.email, password=hash_password(user.password))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


async def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


async def authenticate_user(db: Session, email: str, password: str):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return False
    if not verify_password(plain_password=password,
                           hashed_password=user.password):
        return False
    access_token = create_access_token(data={"sub": user.email,
                                             "user_id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}
