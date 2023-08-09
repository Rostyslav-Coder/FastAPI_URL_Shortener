"""src/crud.py"""

from sqlalchemy.orm import Session

from src import keygen
from src.models import URL
from src.schemas import URLBase


def create_db_url(database: Session, input_url: URLBase) -> URL:
    """Function to create URL in database"""
    user_key = keygen.create_unique_alias(database)
    admin_key = f"{user_key}_{keygen.create_alias(length=8)}"
    created_url = URL(
        target_url=input_url.target_url, user_url=user_key, admin_key=admin_key
    )
    database.add(created_url)
    database.commit()
    database.refresh(created_url)

    return created_url


def get_url_by_key(database: Session, user_key: str) -> URL:
    """Function return URL from database by user URL"""
    return database.query(URL).filter(URL.short_url == user_key, URL.is_active).first()


def get_url_by_admin_key(database: Session, admin_key: str) -> URL:
    """Function return URL from database by admin key"""
    return database.query(URL).filter(URL.admin_url == admin_key, URL.id).first()
