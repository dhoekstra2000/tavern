from sqlalchemy import Column, ForeignKey, Integer, String, Boolean

from .database import Base


class User(Base):
    username = Column(String(32))
    password = Column(String)
