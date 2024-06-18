from sqlalchemy import Column, Integer, ForeignKey, Text
from sqlalchemy.orm import relationship

from db.db_base import Base


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True)
    content = Column(Text)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="post")
