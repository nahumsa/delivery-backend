from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from geoalchemy2.elements import WKTElement
from geoalchemy2.shape import to_shape
from shapely.geometry import mapping
from models import PartnerModel
from schemas import PartnerCreate, Partner


class PartnerRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, partner: PartnerCreate) -> Partner:

        db_partner = PartnerModel(
            trading_name=partner.trading_name,
            owner_name=partner.owner_name,
            document=partner.document,
            coverage_area=WKTElement(partner.coverage_area.wkt, srid=4326),
            address=WKTElement(partner.address.wkt, srid=4326),
        )

        self.db.add(db_partner)

        try:
            self.db.commit()
            self.db.refresh(db_partner)

        except IntegrityError as e:
            self.db.rollback()
            raise e from e

        return Partner(
            id=db_partner.id,
            trading_name=db_partner.trading_name,
            owner_name=db_partner.owner_name,
            document=db_partner.document,  # type: ignore
            coverage_area=mapping(to_shape(db_partner.coverage_area)),  # type: ignore
            address=mapping(to_shape(db_partner.address)),  # type: ignore
        )

    def get_by_id(self, partner_id: int) -> Partner | None:
        db_partner = (
            self.db.query(PartnerModel).filter(PartnerModel.id == partner_id).first()
        )

        if db_partner is None:
            return None

        return Partner(
            id=db_partner.id,
            trading_name=db_partner.trading_name,
            owner_name=db_partner.owner_name,
            document=db_partner.document,  # type: ignore
            coverage_area=mapping(to_shape(db_partner.coverage_area)),  # type: ignore
            address=mapping(to_shape(db_partner.address)),  # type: ignore
        )

    def search_nearest_by_location(
        self, longitude: float, latitude: float
    ) -> Partner | None:
        location = WKTElement(f"POINT({longitude} {latitude})", srid=4326)

        db_partner = (
            self.db.query(PartnerModel)
            .filter(PartnerModel.coverage_area.ST_Contains(location))
            .order_by(PartnerModel.address.ST_Distance(location))
            .first()
        )

        if db_partner is None:
            return None

        return Partner(
            id=db_partner.id,
            trading_name=db_partner.trading_name,
            owner_name=db_partner.owner_name,
            document=db_partner.document,  # type: ignore
            coverage_area=mapping(to_shape(db_partner.coverage_area)),  # type: ignore
            address=mapping(to_shape(db_partner.address)),  # type: ignore
        )
