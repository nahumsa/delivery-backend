# Delivery Backend

This project is a FastAPI-based backend application for managing delivery partners, incorporating geographic data using PostGIS.

## Features

- **Partner Management:** Create and retrieve delivery partner information.
- **Geographic Data:** Utilizes PostGIS for handling coverage areas (MultiPolygon) and addresses (Point).
- **Database Integration:** Uses SQLAlchemy for ORM with PostgreSQL.
- **API Endpoints:** Provides RESTful API endpoints for interaction.

## Technologies Used

- **FastAPI:** Web framework for building APIs.
- **SQLAlchemy:** Python SQL toolkit and Object Relational Mapper.
- **GeoAlchemy2:** Extends SQLAlchemy to work with spatial databases like PostGIS.
- **PostgreSQL/PostGIS:** Relational database with spatial capabilities.
- **Pydantic:** Data validation and settings management.
- **Pytest:** Testing framework.
- **Docker & Docker Compose:** For containerization and orchestration of services.
- **uv:** Fast Python package installer and resolver.

## Setup

Follow these steps to get the project up and running on your local machine.

### 1. Clone the repository

```bash
git clone https://github.com/your-username/delivery-backend.git
cd delivery-backend
```

### 2. Set up Python Environment and Install Dependencies

This project uses `uv` for dependency management. If you don't have `uv` installed, you can install it via `pip` or `curl`:

```bash
# Using pip
pip install uv

# Or using curl (recommended for fresh install)
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Once `uv` is installed, create the virtual environment and install dependencies:

```bash
uv venv
source .venv/bin/activate
uv sync
```

### 3. Set up Database with Docker Compose

Ensure you have Docker and Docker Compose installed. Then, start the database service:

```bash
docker-compose up -d db
```

This will start a PostgreSQL database with PostGIS enabled.

### 4. Run the Application

Once the database is running and your Python dependencies are installed, you can start the FastAPI application:

```bash
make run
```

The API will be accessible at `http://localhost:8000`.

## Running Tests

To run the tests, ensure your database is running via Docker Compose and then use the Makefile:

```bash
make test
```

## Project Structure

- `backend/`: Contains the FastAPI application code, including `main.py`, `models.py`, `database.py`, and `config.py`.
- `database/`: Contains the Dockerfile for the PostgreSQL/PostGIS database.
- `tests/`: Contains unit and integration tests for the application.
- `.github/workflows/`: Contains GitHub Actions workflow for CI/CD.
- `Makefile`: Contains convenient commands for running the application and tests.
- `pyproject.toml`: Project dependencies and metadata.
- `uv.lock`: Lock file for `uv` to ensure reproducible builds.

