.PHONY: test help run

# Database environment variables for testing
DB_VARS := DB_USER=user DB_PASSWORD=password DB_HOST=localhost DB_PORT=5432 DB_NAME=gis_db

# Default target
all: help

help:
	@echo "Available commands:"
	@echo "  make test   - Run Python tests"
	@echo "  make run    - Run the FastAPI application"


test:
	@echo "Running Python tests..."
	$(DB_VARS) uv run pytest

run_db:
	@echo "Running the FastAPI application..."
	docker compose up db -d --build

run_locally: run_db
	@echo "Running the FastAPI application..."
	$(DB_VARS) uv run uvicorn backend.main:app --host 0.0.0.0 --port 9000 --reload

run_docker_compose:
	@echo "Running docker compose"
	docker compose up -d --build
