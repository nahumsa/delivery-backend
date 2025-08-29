from pydantic import BaseModel, ConfigDict
from geojson_pydantic.geometries import Point, MultiPolygon


class PartnerBase(BaseModel):
    trading_name: str
    owner_name: str
    document: str
    coverage_area: MultiPolygon
    address: Point


class PartnerCreate(PartnerBase):
    pass


class Partner(PartnerBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


class PartnerSearch(BaseModel):
    id: int
    trading_name: str
    owner_name: str
    document: str
    coverage_area: MultiPolygon
    address: Point
    distance: float
