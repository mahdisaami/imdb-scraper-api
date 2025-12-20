from sqlalchemy.orm import Session

from app.models import User
from app.services.exceptions import UserNotFoundException


class UserService:
    def __init__(self, db: Session):
        self.db = db

    def get_user_by_username(self, username: str):
        db_user = self.db.query(User).filter(User.username == username).first()
        if not db_user:
            raise UserNotFoundException()
        return db_user

    def get_user_by_id_or_404(self, user_id: int):
        db_user = self.db.query(User).filter(User.id == user_id).first()
        if not db_user:
            raise UserNotFoundException()
        return db_user

    def get_all_users_db(self):
        return self.db.query(User).all()

    def db_delete_commit(self, instance):
        self.db.delete(instance)
        self.db.commit()

    def db_commit_refresh(self, instance):
        self.db.commit()
        self.db.refresh(instance)
        return instance

    def db_add_commit_refresh(self, instance):
        self.db.add(instance)
        self.db.commit()
        self.db.refresh(instance)
        return instance