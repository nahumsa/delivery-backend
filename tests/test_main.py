import pytest
from fastapi.testclient import TestClient
from backend.main import app, get_partner_repository
from backend.schemas import PartnerCreate
from backend.models import PartnerModel
from sqlalchemy.exc import IntegrityError


@pytest.fixture
def client_with_mock_repo():
    app.dependency_overrides[get_partner_repository] = get_test_partner_repository
    yield TestClient(app)
    app.dependency_overrides = {}


class TestPartnerRepository:
    def create(self, partner: PartnerCreate) -> PartnerModel:
        if partner.document == "12345678901234":
            raise IntegrityError(
                "duplicate key value violates unique constraint", "params", "orig"
            )
        return PartnerModel(
            id=1,
            trading_name=partner.trading_name,
            owner_name=partner.owner_name,
            document=partner.document,
            coverage_area=partner.coverage_area,
            address=partner.address,
        )

    def get_by_id(self, partner_id: int) -> PartnerModel | None:
        if partner_id == 1:
            return PartnerModel(
                id=1,
                trading_name="Adega da Cerveja - Pinheiros",
                owner_name="Zé da Silva",
                document="12345678901235",
                coverage_area={
                    "type": "MultiPolygon",
                    "coordinates": [
                        [
                            [
                                [-46.57421, -21.785741],
                                [-46.57421, -21.785741],
                                [-46.57421, -21.785741],
                                [-46.57421, -21.785741],
                            ]
                        ]
                    ],
                },
                address={"type": "Point", "coordinates": [-46.57421, -21.785741]},
            )
        return None

    def search_nearest_by_location(
        self, longitude: float, latitude: float
    ) -> PartnerModel | None:
        if longitude == -46.57421 and latitude == -21.785741:
            return PartnerModel(
                id=1,
                trading_name="Adega da Cerveja - Pinheiros",
                owner_name="Zé da Silva",
                document="12345678901235",
                coverage_area={
                    "type": "MultiPolygon",
                    "coordinates": [
                        [
                            [
                                [-46.57421, -21.785741],
                                [-46.57421, -21.785741],
                                [-46.57421, -21.785741],
                                [-46.57421, -21.785741],
                            ]
                        ]
                    ],
                },
                address={"type": "Point", "coordinates": [-46.57421, -21.785741]},
            )
        return None


def get_test_partner_repository():
    return TestPartnerRepository()


app.dependency_overrides[get_partner_repository] = get_test_partner_repository


def test_read_root(client_with_mock_repo):
    response = client_with_mock_repo.get("/health")
    assert response.status_code == 200


def test_create_partner(client_with_mock_repo):
    response = client_with_mock_repo.post(
        "/partners/",
        json={
            "trading_name": "Adega da Cerveja - Pinheiros",
            "owner_name": "Zé da Silva",
            "document": "12345678901235",
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
    assert data["document"] == "12345678901235"


def test_create_partner_duplicate_document(client_with_mock_repo):
    response = client_with_mock_repo.post(
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
    assert response.status_code == 400
    assert "Document already exists." in response.json()["detail"]


def test_create_partner_unexpected_error(client_with_mock_repo):
    class TestPartnerRepositoryWithUnexpectedError:
        def create(self, partner: PartnerCreate) -> PartnerModel:
            raise IntegrityError("some unexpected error", "params", "orig")

    def get_test_partner_repository_with_unexpected_error():
        return TestPartnerRepositoryWithUnexpectedError()

    app.dependency_overrides[get_partner_repository] = (
        get_test_partner_repository_with_unexpected_error
    )

    response = client_with_mock_repo.post(
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

    assert response.status_code == 500
    assert "some unexpected occured" in response.json()["detail"]


def test_get_partner(client_with_mock_repo):
    response = client_with_mock_repo.get("/partners/1")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert data["trading_name"] == "Adega da Cerveja - Pinheiros"
    assert data["owner_name"] == "Zé da Silva"
    assert data["document"] == "12345678901235"


def test_get_partner_not_found(client_with_mock_repo):
    response = client_with_mock_repo.get("/partners/2")
    assert response.status_code == 404
    assert "Partner not found" in response.json()["detail"]


def test_search_partner(client_with_mock_repo):
    response = client_with_mock_repo.get("/partners?long=-46.57421&lat=-21.785741")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert data["trading_name"] == "Adega da Cerveja - Pinheiros"
    assert data["owner_name"] == "Zé da Silva"
    assert data["document"] == "12345678901235"


def test_search_partner_not_found(client_with_mock_repo):
    response = client_with_mock_repo.get("/partners?long=1.1&lat=1.1")
    assert response.status_code == 404
    assert "Partner not found" in response.json()["detail"]
