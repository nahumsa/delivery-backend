<h1 align="center">Delivery App Backend</h1>
<p align="center">
<a href="https://github.com/nahumsa/delivery-backend/actions"><img alt="Actions Status" src="https://github.com/nahumsa/delivery-backend/actions/workflows/ci.yml/badge.svg"></a>
<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
<a href="https://pycqa.github.io/isort/"><img alt="Imports: isort" src="https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336"></a>
<a href="https://github.com/astral-sh/ruff"><img alt="Ruff" src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json"></a>
</p>

This project is a FastAPI-based backend application for managing delivery partners, incorporating geographic data using PostGIS.

## Features

- **Partner Management:** Create and retrieve delivery partner information.
- **Geographic Search:** Search for the nearest partner based on a given longitude and latitude.
- **Caching:** Uses Redis to cache partner data for faster responses.
- **Database Integration:** Uses SQLAlchemy and GeoAlchemy2 for ORM with PostgreSQL/PostGIS.
- **API Endpoints:** Provides RESTful API endpoints for creating, retrieving, and searching for partners.
- **Health Check:** A dedicated endpoint to check the health of the application.
- **Caching:** All requests are cached to improve performance. It has been used Geohash to cache the latitude and longitude for the search of partners.

## API Endpoints

- `POST /partners/`: Creates a new partner.
- `GET /partners/{partner_id}`: Retrieves a partner by ID.
- `GET /partners`: Searches for the nearest partner by longitude and latitude.
- `GET /health`: Health check endpoint.

## Technologies Used

- **FastAPI:** Web framework for building APIs.
- **SQLAlchemy:** Python SQL toolkit and Object Relational Mapper.
- **GeoAlchemy2:** Extends SQLAlchemy to work with spatial databases like PostGIS.
- **PostgreSQL/PostGIS:** Relational database with spatial capabilities.
- **Redis:** Added for caching.
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
