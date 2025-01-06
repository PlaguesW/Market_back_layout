
from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserCreate

def create_user(db: Session, user_in: UserCreate) -> User:
    """
    Create user and save it to the database
    """
    db_user = User(
        email=user_in.email,
        full_name=user_in.full_name,

        hashed_password=user_in.password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_all_users(db: Session) -> list[User]:
    """
    Retrieve all users from the database
    """
    return db.query(User).all()