"""src/crud.py"""

from sqlalchemy.orm import Session

from src import models, schemas, short_url_gen


def create_db_url(db: Session, url: schemas.URLBase) -> models.URL:
    """Function create URL in database"""
    random_user_url = short_url_gen.create_random_url()
    random_admin_url = short_url_gen.create_random_url(length=8)
    db_url = models.URL(
        target_url=url.target_url, user_url=random_user_url, admin_url=random_admin_url
    )
    db.add(db_url)
    db.commit()
    db.refresh(db_url)

    return db_url


def get_db_url_by_user_url(db: Session, user_url: str) -> models.URL:
    """Function return URL from database by user URL"""
    return (
        db.query(models.URL)
        .filter(models.URL.user_url == user_url, models.URL.is_active)
        .first()
    )
