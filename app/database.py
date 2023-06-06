import uuid
import logging

from sqlalchemy import create_engine, Column, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.dialects.postgresql import UUID

from app.settings import settings

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


class PkModel(object):
    """
    Base model with UUID4 primary key
    """

    id = Column(
        UUID(as_uuid=False), primary_key=True, default=lambda: str(uuid.uuid4())
    )


class CRUDMixin(object):
    """
    Helper class with CRUD utilities
    """

    @classmethod
    def create(cls, db: Session, commit=True, **kwargs):
        instance = cls(**kwargs)
        return instance.save(db, commit=commit)

    def save(self, db: Session, commit=True):
        db.add(self)

        if commit:
            db.commit()
        else:
            db.flush()
            db.refresh(self)

        return self

    @classmethod
    def get_by_id(cls, db: Session, id):
        return db.query(cls).filter(cls.id == id).first()

    def update(self, db: Session, commit=True, **kwargs):
        for attr, value in kwargs.items():
            setattr(self, attr, value)

        return commit and self.save(db) or self

    def delete(self, db: Session, commit=True):
        """Hard delete from DB"""
        db.delete(self)
        return commit and db.commit()


def foreign_key_column(column_name, on_delete="CASCADE", **kwargs):
    """Helper for mounting a foreign key column"""
    return Column(
        UUID(as_uuid=False), ForeignKey(column_name, ondelete=on_delete), **kwargs
    )
