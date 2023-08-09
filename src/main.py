"""src/main.py"""

import validators
from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from src import crud, models, schemas
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


def raise_bad_request(message):
    """Function to raise bad request exceptions"""
    raise HTTPException(status_code=400, detail=message)


def raise_not_found(request):
    """Function to raise not found exceptions"""
    message = f"URL '{request.url}' doesn`t exist"
    raise HTTPException(status_code=404, detail=message)


@app.get("/", name="Welcome page")
def root():
    """Function that sends a welcome message"""
    return "Welcome to the URL shortener API :)"


@app.post("/url", response_model=schemas.URLOut, name="Create URL")
def create_url(input_url: schemas.URLBase, db: Session = Depends(get_db)):
    """Function to create entry in database"""
    if not validators.url(input_url.target_url):
        raise_bad_request(message="Your URL is not valid")

    db_url = crud.create_db_url(db=db, url=input_url)
    db_url.user_url = db_url.user_url
    db_url.admin_url = db_url.admin_url

    return db_url


@app.get("/url/{input_url}", name="Redirect to URL")
def redirect_to_target_url(
    input_url: str, request: Request, db: Session = Depends(get_db)
):
    """Function that take user Url & redirect User to target Url"""
    if db_url := crud.get_url_by_input_url(db=db, user_url=input_url):
        return RedirectResponse(db_url.target_url)
    raise_not_found(request)


@app.get("/admin/{input_admin_url}", response_model=schemas.URLOut, name="admin info")
def get_url_info(input_admin_url: str, request: Request, db: Session = Depends(get_db)):
    """Function get URL by admin url"""
    if db_url := crud.get_url_by_admin_url(db, input_admin_url=input_admin_url):
        db_url.short_url = db_url.short_url
        db_url.admin_url = db_url.admin_url
        return db_url
    raise_not_found(request)
