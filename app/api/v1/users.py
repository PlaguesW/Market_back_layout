
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.user import UserCreate, UserRead
from app.services.user_service import create_user, get_all_users

router = APIRouter()

@router.post("/", response_model=UserRead)
def create_new_user(user_in: UserCreate, db: Session = Depends(get_db)):
    """
    Create a new user in the database
    """
    user = create_user(db, user_in)
    return user

@router.get("/", response_model=list[UserRead])
def list_all_users(db: Session = Depends(get_db)):
    """
    Get a list of all users
    """
    return get_all_users(db)