"""src/crud.py"""

from sqlalchemy.orm import Session

from src import models, schemas, short_url_gen


def create_db_url(db: Session, url: schemas.URLBase) -> models.URL:
    random_user_url = short_url_gen.create_random_url()
    random_admin_url = short_url_gen.create_random_url(length=8)
    db_url = models.URL(
        target_url=url.target_url, user_url=random_user_url, admin_url=random_admin_url
    )
    db.add(db_url)
    db.commit()
    db.refresh(db_url)

    return db_url
