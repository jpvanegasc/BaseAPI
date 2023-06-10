import logging

from typing import List

from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, Session, declarative_base, Query
from sqlalchemy.exc import IntegrityError

from app.settings import settings


logger = logging.getLogger("logger")

POSTGRES_INDEXES_NAMING_CONVENTION = {
    "ix": "%(column_0_label)s_idx",
    "uq": "%(table_name)s_%(column_0_name)s_key",
    "ck": "%(table_name)s_%(constraint_name)s_check",
    "fk": "%(table_name)s_%(column_0_name)s_fkey",
    "pk": "%(table_name)s_pkey",
}
metadata = MetaData(naming_convention=POSTGRES_INDEXES_NAMING_CONVENTION)


engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=True, bind=engine)
Base = declarative_base(metadata=metadata)


def db_session() -> Session:
    try:
        db: Session = SessionLocal()
        yield db
    except Exception:
        logger.critical("DB is down", exc_info=True)
        raise
    finally:
        db.close()


def paginate(query: Query, page_number: int, per_page: int) -> List:
    offset = (page_number - 1) * per_page
    return query.limit(per_page).offset(offset).all()


def commit_if_unique(db: Session, exception=Exception, msg="duplicate resource"):
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise exception(msg)
