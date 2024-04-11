import logging
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session, declarative_base

from app.config import settings

logger = logging.getLogger(__name__)

engine = create_engine(settings.database_url())
SessionMaker = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def db_session() -> Generator[Session, None, None]:
    try:
        db: Session = SessionMaker()
        yield db
    finally:
        db.close()
