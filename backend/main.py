from fastapi import FastAPI, Depends
from fastapi import status
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
import schemas
import database
from repositories import PartnerRepository


app = FastAPI()

db = database.get_db()


def get_partner_repository() -> PartnerRepository:
    return PartnerRepository(db)


@app.get("/health")
def read_root():
    return


@app.post("/partners/", response_model=schemas.Partner)
def create_partner(
    partner: schemas.PartnerCreate,
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
