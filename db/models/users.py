from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship

from db.db_base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String(255))
    password = Column(String(255))

    post = relationship("Post", back_populates="user")
