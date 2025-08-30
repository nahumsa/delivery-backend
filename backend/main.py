from fastapi import FastAPI, Depends
from fastapi import status
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from schemas import Partner, PartnerCreate
from database import get_db
from repositories import PartnerRepository


app = FastAPI()


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
):
    db_partner = partner_repo.get_by_id(partner_id)
    if db_partner is None:
        raise HTTPException(status_code=404, detail="Partner not found")
    return db_partner
