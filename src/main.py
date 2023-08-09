"""src/main.py"""

from fastapi import FastAPI

app = FastAPI()


@app.get("/", name="Welcome page")
def root():
    """Function that sends a welcome message"""
    return "Welcome to the URL shortener API :)"
