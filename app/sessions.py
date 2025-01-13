from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker, Session
from fastapi import Depends
from typing import Generator

# Database URL configuration
url = URL.create(
    drivername="postgresql",
    username="postgres",
    password="1453",
    host="localhost",
    port=5432,
    database="sales_office"
)

# Create SQLAlchemy engine
engine = create_engine(url)

# Create a session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency for getting the session
def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
