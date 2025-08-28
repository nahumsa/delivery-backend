from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
import models, database
from geoalchemy2.elements import WKTElement
from geoalchemy2.shape import to_shape
from shapely.geometry import mapping


app = FastAPI()

database.Base.metadata.create_all(bind=database.engine)


@app.get("/health")
def read_root():
    return 


@app.post("/partners/", response_model=models.Partner)
def create_partner(
    partner: models.PartnerCreate, db: Session = Depends(database.get_db)
):
    db_partner = database.Partner(
        trading_name=partner.trading_name,
        owner_name=partner.owner_name,
        document=partner.document,
        coverage_area=WKTElement(partner.coverage_area.wkt, srid=4326),
        address=WKTElement(partner.address.wkt, srid=4326),
    )
    db.add(db_partner)
    db.commit()
    db.refresh(db_partner)
    return models.Partner(
        id=db_partner.id,
        trading_name=db_partner.trading_name,
        owner_name=db_partner.owner_name,
        document=db_partner.document,
        coverage_area=mapping(to_shape(db_partner.coverage_area)),
        address=mapping(to_shape(db_partner.address)),
    )
