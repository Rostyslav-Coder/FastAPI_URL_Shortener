"""src/models.py"""

from sqlalchemy import Boolean, Column, Integer, String

from src.database import Base


class URL(Base):
    """Class to init database table URL"""

    __teblaname__ = "urls"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_url = Column(String, unique=True, index=True)
    admin_url = Column(String, unique=True, index=True)
    target_url = Column(String, index=True)
    is_active = Column(Boolean, default=True)
    clicks = Column(Integer, default=0)
