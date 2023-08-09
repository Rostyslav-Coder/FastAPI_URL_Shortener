"""src/short_url_gen.py"""

import secrets
import string

from sqlalchemy.orm import Session

from src import crud


def create_random_url(length: int = 5) -> str:
    """Function to generate random short URL"""
    chars = string.ascii_uppercase + string.digits

    return "".join(secrets.choice(chars) for _ in range(length))


def create_unique_random_url(db: Session) -> str:
    """Function generate only unique URL"""
    unique_url = create_random_url()
    while crud.get_db_url_by_input_url(db, unique_url):
        unique_url = create_random_url()
    return unique_url
