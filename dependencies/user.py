from fastapi.security import OAuth2PasswordBearer

from config import secret_key, algorithm
from typing import Optional

import jwt
from fastapi import HTTPException, Depends

from starlette import status

from schemas.users import Token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_current_user(token: str = Depends(oauth2_scheme)):
    user = verify_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )
    return user


def verify_token(token: str) -> Optional[Token]:
    try:
        payload = jwt.decode(token, secret_key, algorithms=[algorithm])
        mail = payload.get("sub")
        user_id = payload.get("user_id")
        if mail is None:
            return None
        token_data = Token(id=user_id,
                           mail=mail)
        return token_data
    except jwt.PyJWTError:
        return None
