from geoalchemy2 import Geometry, WKBElement
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Mapped, declarative_base, mapped_column

Base = declarative_base()


class PartnerModel(Base):
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
