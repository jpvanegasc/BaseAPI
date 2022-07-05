from sqlalchemy.orm import Session


class UndefinedModelError(Exception):
    pass


class BaseCRUD(object):
    model = None

    def __init__(self):
        if self.model is None:
            raise UndefinedModelError(
                f"model for class '{type(self).__name__}' not set"
            )

    def create(self, db: Session, data: dict):
        return self.model.create(db, **data)

    def all(self, db: Session):
        return db.query(self.model).all()

    def get_by_id(self, db: Session, id: str):
        return self.model.get_by_id(db, id)

    def update(self, db: Session, id: str, update_data: dict):
        return self.model.get_by_id(db, id).update(db, **update_data)

    def delete(self, db: Session, user_id: str):
        """Hard delete from DB"""
        return self.model.get_by_id(db, user_id).delete(db)
