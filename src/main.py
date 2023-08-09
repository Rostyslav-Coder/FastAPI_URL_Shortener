"""src/main.py"""

import secrets

import validators
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from src import models, schemas
from src.database import SessionLocal, engine

app = FastAPI()
models.Base.metadata.create_all(bind=engine)


def get_db():
    """Database session controler"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def raise_bad_request_msg(message):
    """Function to raise HTTP Exceptions"""
    raise HTTPException(status_code=400, detail=message)


@app.get("/", name="Welcome page")
def root():
    """Function that sends a welcome message"""
    return "Welcome to the URL shortener API :)"


@app.post("/url", response_model=schemas.URLOut, name="Create URL")
def create_url(url: schemas.URLBase, db: Session = Depends(get_db)):
    """Function to create entry in database"""
    if not validators.url(url.target_url):
        raise_bad_request_msg(message="Your URL is not valid")

    chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    user_url = "".join(secrets.choice(chars) for _ in range(5))
    admin_url = "".join(secrets.choice(chars) for _ in range(8))
    db_url = models.URL(
        target_url=url.target_url, user_url=user_url, admin_url=admin_url
    )

    db.add(db_url)
    db.commit()
    db.refresh(db_url)
    db_url.user_url = user_url
    db_url.admin_url = admin_url

    return db_url
