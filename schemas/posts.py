from fastapi import HTTPException
from pydantic import BaseModel, field_validator


class PostBase(BaseModel):
    content: str

    @field_validator('content')
    def validate_content_size(cls, content):
        # Check the size of the content (1 MB = 1_000_000 bytes)
        if len(content.encode()) > 1_000_000:
            raise HTTPException(status_code=413, detail="Payload too large")
        return content


class PostCreate(PostBase):
    pass


class Post(PostBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True
