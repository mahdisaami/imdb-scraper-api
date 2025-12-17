from sqlalchemy.orm import Session

from app.core.security import SECRET_KEY, ALGORITHM
from app.deps import oauth2_scheme, get_db
from app.models import User
from fastapi import Depends, HTTPException
from jose import JWTError, jwt


def get_user_by_username(db: Session, username: str):
    return (
        db.query(User)
        .filter(User.username == username)
        .first()
    )



def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if not username:
            raise HTTPException(status_code=401)
    except JWTError:
        raise HTTPException(status_code=401)

    return get_user_by_username(username=username,db=db )
