"""src/main.py"""

import secrets

import validators
from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import RedirectResponse
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
    """Function to raise bad request exceptions"""
    raise HTTPException(status_code=400, detail=message)


def raise_not_found_msg(request):
    """Function to raise not found exceptions"""
    message = f"URL '{request.url}' doesn`t exist"
    raise HTTPException(status_code=404, detail=message)


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


@app.get("/url/{user_url}", name="Redirect to URL")
def redirect_to_target_url(
    user_url: str, request: Request, db: Session = Depends(get_db)
):
    """Function that take user Url & redirect User to target Url"""
    db_url = (
        db.query(models.URL)
        .filter(models.URL.user_url == user_url, models.URL.is_active)
        .first()
    )

    if not db_url:
        raise_not_found_msg(request)
    return RedirectResponse(db_url.target_url)
