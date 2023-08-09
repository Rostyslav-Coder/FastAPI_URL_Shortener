"""src/main.py"""

import validators
from fastapi import FastAPI, HTTPException

from src import schemas

app = FastAPI()


def raise_bad_request_msg(message):
    """Function to raise HTTP Exceptions"""
    raise HTTPException(status_code=400, detail=message)


@app.get("/", name="Welcome page")
def root():
    """Function that sends a welcome message"""
    return "Welcome to the URL shortener API :)"


@app.post("/url", name="Create URL")
def create_url(url: schemas.URLBase):
    """Function to create entry in database"""
    if not validators.url(url.target_url):
        raise_bad_request_msg(message="Your URL is not valid")
    return f"TODO: Create database entry for {url.target_url}"
