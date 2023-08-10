"""src/crud.py"""

from sqlalchemy.orm import Session

from src import keygen
from src.models import URL
from src.schemas import URLBase, URLIn


def create_db_url(database: Session, url: URLBase) -> URL:
    """Function to create URL in database"""
    user_key = keygen.create_unique_alias(database)
    secret_key = f"{user_key}_{keygen.create_alias(length=8)}"
    created_url = URL(
        target_url=url.target_url,
        short_url=user_key,
        admin_key=secret_key,
    )
    database.add(created_url)
    database.commit()
    database.refresh(created_url)

    return created_url


def get_url_by_key(database: Session, short_url: str) -> URL:
    """Function return URL from database by user URL"""
    return (
        database.query(URL)
        .filter(URL.short_url == short_url, URL.is_active)
        .first()
    )


def get_url_by_admin_key(database: Session, secret_key: str) -> URL:
    """Function return URL from database by admin key"""
    return (
        database.query(URL)
        .filter(URL.admin_url == secret_key, URL.is_active)
        .first()
    )


def update_db_clicks(database: Session, db_url: URLIn) -> URL:
    db_url.clicks += 1
    database.commit()
    database.refresh(db_url)
    return db_url


def deactivate_url_by_secret_key(database: Session, secret_key: str) -> URL:
    db_url = get_url_by_admin_key(database=database, secret_key=secret_key)
    if db_url:
        db_url.is_active = False
        database.commit()
        database.refresh(db_url)
    return db_url
