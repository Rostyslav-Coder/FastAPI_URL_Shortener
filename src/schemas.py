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

        orm_mode = True


class URLOut(URLIn):
    """Outer class URL"""

    user_url: str
    admin_url: str
