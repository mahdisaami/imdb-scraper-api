from app.db.base import Base
from app.db.session import engine
from app.models.user_model import User

# Base.metadata.create_all(bind=engine)