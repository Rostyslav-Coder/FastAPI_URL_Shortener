"""src/short_url_gen.py"""

import secrets
import string


def create_random_url(length: int = 5) -> str:
    """Function to generate random short URL"""
    chars = string.ascii_uppercase + string.digits

    return "".join(secrets.choice(chars) for _ in range(length))
