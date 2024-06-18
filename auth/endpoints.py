from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from starlette import status

from dependencies.db import get_db
from schemas.users import UserCreate
from . import cruds
from .helpers import create_access_token

auth_router = APIRouter(
)


@auth_router.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(),
                                 db: Session = Depends(get_db)):
    user = await cruds.authenticate_user(db=db, email=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return {"access_token": user["access_token"], "token_type": "bearer"}


@auth_router.post("/register")
async def registration(user: UserCreate,
                       db: Session = Depends(get_db)):
    user = await cruds.create_user(db=db,
                                   user=user)

    if user:
        return {"token": create_access_token({"sub": user.email})}
