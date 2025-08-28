from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Mapped, mapped_column
from geoalchemy2 import Geometry, WKBElement
from config import settings

engine = create_engine(settings.database_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class Partner(Base):
    __tablename__ = "partners"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    trading_name: Mapped[str] = mapped_column(String(50))
    owner_name: Mapped[str] = mapped_column(String(256))
    document = Column(String, unique=True, index=True)
    coverage_area: Mapped[WKBElement] = mapped_column(
        Geometry(geometry_type="MULTIPOLYGON", srid=4326)
    )
    address: Mapped[WKBElement] = mapped_column(
        Geometry(geometry_type="POINT", srid=4326, spatial_index=True)
    )


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
