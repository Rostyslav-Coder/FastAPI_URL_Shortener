"""src/short_url_gen.py"""

import secrets
import string

from sqlalchemy.orm import Session

from src import crud


def create_alias(length: int = 5) -> str:
    """Function to generate random short URL"""
    chars = string.ascii_uppercase + string.digits

    return "".join(secrets.choice(chars) for _ in range(length))


def create_unique_alias(database: Session) -> str:
    """Function generate only unique URL"""
    unique_url = create_alias()
    while crud.get_url_by_short(database, unique_url):
        unique_url = create_alias()
    return unique_url
