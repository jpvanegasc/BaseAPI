from sqlalchemy.orm.session import Session

from app.services.common import BaseCRUD
import app.models.user as user_models


class UserCRUD(BaseCRUD):
    model = user_models.User

    def get_by_username(self, db: Session, username: str):
        return (
            db.query(user_models.User)
            .filter(user_models.User.username == username)
            .first()
        )
