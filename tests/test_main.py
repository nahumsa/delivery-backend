from fastapi.testclient import TestClient
from backend.main import app
from backend.database import SessionLocal, Base, engine
import pytest

client = TestClient(app)

@pytest.fixture(name="db")
def db_fixture():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


def test_read_root():
    response = client.get("/health")
    assert response.status_code == 200


def test_create_partner(db):
    response = client.post(
        "/partners/",
        json={
            "trading_name": "Adega da Cerveja - Pinheiros",
            "owner_name": "Zé da Silva",
            "document": "12345678901234",
            "coverage_area": {
                "type": "MultiPolygon",
                "coordinates": [
                    [
                        [
                            [30, 20],
                            [45, 40],
                            [10, 40],
                            [30, 20],
                        ]
                    ]
                ],
            },
            "address": {"type": "Point", "coordinates": [-46.57421, -21.785741]},
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["trading_name"] == "Adega da Cerveja - Pinheiros"
    assert data["owner_name"] == "Zé da Silva"
    assert data["document"] == "12345678901234"


def test_create_partner_duplicate_document(db):
    # Create the first partner
    response = client.post(
        "/partners/",
        json={
            "trading_name": "Adega da Cerveja - Pinheiros",
            "owner_name": "Zé da Silva",
            "document": "12345678901234",
            "coverage_area": {
                "type": "MultiPolygon",
                "coordinates": [
                    [
                        [
                            [30, 20],
                            [45, 40],
                            [10, 40],
                            [30, 20],
                        ]
                    ]
                ],
            },
            "address": {"type": "Point", "coordinates": [-46.57421, -21.785741]},
        },
    )
    assert response.status_code == 200

    # Attempt to create a second partner with the same document
    response = client.post(
        "/partners/",
        json={
            "trading_name": "Another Trading Name",
            "owner_name": "Another Owner",
            "document": "12345678901234",  # Duplicate document
            "coverage_area": {
                "type": "MultiPolygon",
                "coordinates": [
                    [
                        [
                            [30, 20],
                            [45, 40],
                            [10, 40],
                            [30, 20],
                        ]
                    ]
                ],
            },
            "address": {"type": "Point", "coordinates": [-46.57421, -21.785741]},
        },
    )
    assert response.status_code == 400
    assert "Document already exists." in response.json()["detail"]
