from datetime import datetime

from click import echo
from sqlalchemy import Column, DateTime, Integer, create_engine
from sqlalchemy.orm import (declarative_base, declared_attr, scoped_session,
                            sessionmaker)

engine = create_engine("postgresql://douwe:123456@localhost:5432/tavern2", echo=True)
db_session = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine)
)


class CustomBase:
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    date_created = Column(DateTime, default=datetime.utcnow)
    date_updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


Base = declarative_base(cls=CustomBase)
Base.query = db_session.query_property()
