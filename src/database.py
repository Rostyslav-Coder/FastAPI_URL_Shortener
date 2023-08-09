"""src/database.py"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from src.config import get_settings

# Database entry point
engine = create_engine(get_settings().db_url, connect_args={"check_same_thread": False})

# Database working session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Parent database class
Base = declarative_base()
