import logging

import pygeohash
from cache_repository import CacheRepository
from fastapi import Depends, FastAPI, HTTPException, status
from logging_config import LogConfig
from repositories import PartnerRepository
from schemas import Partner, PartnerCreate
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from database import get_db

LogConfig.setup_logging()

app = FastAPI()


def get_cache_repository() -> CacheRepository:
    return CacheRepository()


def get_partner_repository(db: Session = Depends(get_db)) -> PartnerRepository:
    return PartnerRepository(db)


@app.get("/health")
def read_root():
    return


@app.post("/partners/", response_model=Partner)
def create_partner(
    partner: PartnerCreate,
    partner_repo: PartnerRepository = Depends(get_partner_repository),
):
    try:
        db_partner = partner_repo.create(partner)

    except IntegrityError as e:
        if "duplicate key value violates unique constraint" in str(e):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Document already exists.",
            )

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="some unexpected occured",
        )

    return db_partner


@app.get("/partners/{partner_id}", response_model=Partner)
def get_partner(
    partner_id: int,
    partner_repo: PartnerRepository = Depends(get_partner_repository),
    cache_repo: CacheRepository = Depends(get_cache_repository),
):
    logging.info(f"Fetching partner for id: {partner_id}")
    cached_partner = cache_repo.get(f"partner_{partner_id}")

    if cached_partner:
        logging.info(f"Partner found in cache for id: {partner_id}")
        return Partner.model_validate(cached_partner)

    logging.info(f"Partner not found in cache for id: {partner_id}, fetching from db")
    db_partner = partner_repo.get_by_id(partner_id)
    if db_partner is None:
        logging.error(f"Partner not found for id: {partner_id}")
        raise HTTPException(status_code=404, detail="Partner not found")

    logging.info(f"Partner found in db for id: {partner_id}, caching result")
    cache_repo.set(f"partner_{partner_id}", db_partner.model_dump(), 3600)

    return db_partner


@app.get("/partners", response_model=Partner)
def search_partner(
    long: float,
    lat: float,
    partner_repo: PartnerRepository = Depends(get_partner_repository),
    cache_repo: CacheRepository = Depends(get_cache_repository),
):

    geohash = pygeohash.encode(latitude=lat, longitude=long)

    logging.info(f"Fetching partner for geohash: {geohash}")
    cached_partner = cache_repo.get(f"partner_{geohash}")

    if cached_partner:
        logging.info(f"Fetching partner for geohash: {geohash}")
        return Partner.model_validate(cached_partner)

    db_partner = partner_repo.search_nearest_by_location(long, lat)
    if db_partner is None:
        raise HTTPException(status_code=404, detail="Partner not found")

    logging.info(f"Partner found in db for geohash: {geohash}, caching result")
    cache_repo.set(f"partner_{geohash}", db_partner.model_dump(), 3600)

    return db_partner
