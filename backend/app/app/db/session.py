from sqlmodel import Field, SQLModel, create_engine
from sqlmodel import Session as SQLModelSession
from contextlib import contextmanager

from app.core.config import settings

engine = create_engine(settings.SQLALCHEMY_DATABASE_URI, pool_pre_ping=True)

@contextmanager
def Session():
    session = SQLModelSession(engine)
    try:
        yield session
    finally:
        session.close()