"""src/schemas.py"""

from pydantic import BaseModel


class URLBase(BaseModel):
    """Parent URL class"""

    target_url: str


class URLIn(URLBase):
    """Inner class URL"""

    is_active: bool
    clicks: int

    class Config:
        """Inner configuration class"""

        from_attributes = True


class URLOut(URLIn):
    """Outer class URL"""

    short_url: str
    admin_key: str
