"""src/main.py"""

import validators
from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from src.crud import create_db_url, get_url_by_key, get_url_by_admin_key
from src.database import SessionLocal, engine
from src.models import Base
from src.schemas import URLBase, URLOut

app = FastAPI()

Base.metadata.create_all(bind=engine)


def get_db():
    """Database session controler"""
    database = SessionLocal()
    try:
        yield database
    finally:
        database.close()


def call_bad_request(message):
    """Function to raise bad request exceptions"""
    raise HTTPException(status_code=400, detail=message)


def call_not_found(request):
    """Function to raise not found exceptions"""
    message = f"URL '{request.url}' doesn`t exist"
    raise HTTPException(status_code=404, detail=message)


@app.get("/", name="Welcome page")
def root():
    """Function that sends a welcome message"""
    return "Welcome to the URL shortener API :)"


@app.post("/url", response_model=URLOut, name="Create URL")
def create_url(user_input: URLBase, data_b: Session = Depends(get_db)):
    """Function to create entry in database"""
    if not validators.url(user_input.target_url):
        call_bad_request(message="Your URL is not valid")

    db_url = create_db_url(database=data_b, input_url=user_input)
    db_url.short_url = db_url.short_url
    db_url.admin_key = db_url.admin_key

    return db_url


@app.get("/url/{input_url}", name="Redirect to URL")
def redirect_to_target_url(
    input_url: str, request: Request, data_b: Session = Depends(get_db)
):
    """Function that take user Url & redirect User to target Url"""
    db_url = get_url_by_key(database=data_b, user_key=input_url)

    if not db_url:
        call_not_found(request)

    return RedirectResponse(db_url.target_url)


@app.get("/admin/{input_admin_url}", response_model=URLOut, name="admin info")
def get_url_info(
    input_admin_key: str, request: Request, data_b: Session = Depends(get_db)
):
    """Function get URL by admin url"""
    db_url = get_url_by_admin_key(database=data_b, admin_key=input_admin_key)

    if not db_url:
        call_not_found(request)

    db_url.short_url = db_url.short_url
    db_url.admin_key = db_url.admin_key

    return db_url
