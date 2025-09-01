from typing import Any, Generator

from config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

engine = create_engine(settings.database_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator[Session, Any, Any]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
