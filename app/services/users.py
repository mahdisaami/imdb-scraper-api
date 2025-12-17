from sqlalchemy.orm import Session

from app.models import User
from app.services.exceptions import UserNotFoundException


def get_user_by_username(db: Session, username: str):
    db_user = db.query(User).filter(User.username == username).first()
    if not db_user:
        raise UserNotFoundException()
    return db_user


def get_user_by_id_or_404(user_id: int, db: Session):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise UserNotFoundException()
    return db_user


def get_all_users_db(db: Session):
    return db.query(User).all()


def db_delete_commit(db: Session, instance):
    db.delete(instance)
    db.commit()

def db_commit_refresh(db: Session, instance):
    db.commit()
    db.refresh(instance)
    return instance

def db_add_commit_refresh(db: Session, instance):
    db.add(instance)
    db.commit()
    db.refresh(instance)
    return instance

