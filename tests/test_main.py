import pytest
from fastapi.testclient import TestClient
from backend.main import app, get_partner_repository, get_cache_repository
from backend.schemas import PartnerCreate, Partner
from backend.models import PartnerModel
from sqlalchemy.exc import IntegrityError
from unittest.mock import MagicMock


@pytest.fixture
def client_with_mock_repo():
    app.dependency_overrides[get_partner_repository] = get_test_partner_repository
    app.dependency_overrides[get_cache_repository] = get_test_cache_repository
    yield TestClient(app)
    app.dependency_overrides = {}


class MockCacheRepository:
    def __init__(self):
        self.cache = {}

    def get(self, key: str):
        return self.cache.get(key)

    def set(self, key: str, value: dict, ex: int):
        self.cache[key] = value


class TestPartnerRepository:
    def create(self, partner: PartnerCreate) -> PartnerModel:
        if partner.document == "12345678901234":
            raise IntegrityError(
                "duplicate key value violates unique constraint", "params", "orig" # type: ignore
            )
        return PartnerModel(
            id=1,
            trading_name=partner.trading_name,
            owner_name=partner.owner_name,
            document=partner.document,
            coverage_area=partner.coverage_area,
            address=partner.address,
        )

    def get_by_id(self, partner_id: int) -> Partner | None:
        if partner_id == 1:
            return Partner(
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
    ) -> Partner | None:
        if longitude == -46.57421 and latitude == -21.785741:
            return Partner(
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

def get_test_cache_repository():
    return MockCacheRepository()


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
            raise IntegrityError("some unexpected error", "params", "orig") # type: ignore

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


def test_get_partner_with_cache(client_with_mock_repo):
    # Arrange
    partner_repo = TestPartnerRepository()
    cache_repo = MockCacheRepository()
    app.dependency_overrides[get_partner_repository] = lambda: partner_repo
    app.dependency_overrides[get_cache_repository] = lambda: cache_repo

    partner_repo.get_by_id = MagicMock(wraps=partner_repo.get_by_id)
    cache_repo.get = MagicMock(wraps=cache_repo.get)
    cache_repo.set = MagicMock(wraps=cache_repo.set)

    # Act
    response1 = client_with_mock_repo.get("/partners/1")
    response2 = client_with_mock_repo.get("/partners/1")

    # Assert
    assert response1.status_code == 200
    assert response2.status_code == 200
    data1 = response1.json()
    data2 = response2.json()
    assert data1 == data2
    partner_repo.get_by_id.assert_called_once_with(1)
    assert cache_repo.get.call_count == 2
    cache_repo.set.assert_called_once()
