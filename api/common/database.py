import logging

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

from api.common import settings

logger = logging.getLogger("logger")

engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=True, bind=engine)
Base = declarative_base()


def db_session() -> Session:
    try:
        db: Session = SessionLocal()
        yield db
    except Exception:
        logger.critical("DB is down", exc_info=True)
    finally:
        db.close()
