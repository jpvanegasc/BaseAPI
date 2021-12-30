from fastapi import HTTPException
from sqlalchemy.orm.session import Session

import api.models.user as user_models
import api.schemas.user as user_schemas


def create_user(db: Session, user_data: dict):
    return user_models.User.create(db, **user_data)


def get_all_users(db: Session):
    return db.query(user_models.User).all()


def get_user_by_id(db: Session, user_id: str):
    return user_models.User.get_by_id(db, user_id)


def get_user_by_username(db: Session, username: str):
    return (
        db.query(user_models.User).filter(user_models.User.username == username).first()
    )


def edit_user(db: Session, user_id: str, update_data: dict):
    return user_models.User.get_by_id(db, user_id).update(db, **update_data)


def delete_user(db: Session, user_id: str):
    """Hard delete from DB"""
    return user_models.User.get_by_id(db, user_id).delete(db)
