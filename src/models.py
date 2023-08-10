"""src/models.py"""

from sqlalchemy import Boolean, Column, Integer, String

from src.database import Base


class URL(Base):
    """Class to create table 'urls' in database"""

    __tablename__ = "urls"

    id = Column(Integer, primary_key=True, autoincrement=True)
    short_url = Column(String, unique=True, index=True)
    admin_info = Column(String, unique=True, index=True)
    target_url = Column(String, index=True)
    is_active = Column(Boolean, default=True)
    clicks = Column(Integer, default=0)
