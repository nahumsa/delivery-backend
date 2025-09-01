import json
from unittest.mock import MagicMock

from backend.cache_repository import CacheRepository


def test_get_from_cache():
    # Arrange
    mock_redis_client = MagicMock()
    mock_redis_client.get.return_value = json.dumps({"key": "value"})

    cache_repo = CacheRepository()
    cache_repo.client = mock_redis_client

    # Act
    result = cache_repo.get("test_key")

    # Assert
    assert result == {"key": "value"}
    mock_redis_client.get.assert_called_once_with("test_key")


def test_set_to_cache():
    # Arrange
    mock_redis_client = MagicMock()
    cache_repo = CacheRepository()
    cache_repo.client = mock_redis_client

    # Act
    cache_repo.set("test_key", {"key": "value"}, 3600)

    # Assert
    mock_redis_client.set.assert_called_once_with(
        "test_key", json.dumps({"key": "value"}), ex=3600
    )
