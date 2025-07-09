# Movie-Actor Filmography Management System

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.0+-green.svg)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-1.4-orange.svg)
![Docker](https://img.shields.io/badge/Docker-Compatible-brightgreen.svg)

## Project Description

A RESTful API for managing actor-film relationships with the following features:

* CRUD operations for actors and movies
* Establishing relationships between actors and films
* Comprehensive filmography management
* Robust error handling and data validation

## Features

✅ Actor management system
✅ Movie database integration
✅ Relationship mapping between actors and films
✅ JSON API responses
✅ Error handling with appropriate HTTP status codes
✅ Docker container support

## Requirements

* Python 3.8+
* Flask 2.0+
* Flask-SQLAlchemy
* Docker (optional)

## Installation

```bash
# Clone repository
git clone https://github.com/yourusername/movie-actor-api.git
cd movie-actor-api

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Docker Containerization

You can run this API using Docker for consistent deployment.

### Build Docker Image

```bash
docker build -t docker build -t <user-name>/<name-of-the-container>:<tag-name> .
```

### Run Docker Container

Make sure your PostgreSQL database is running and accessible. Run the container using:

```bash
docker run \
  --env DB_URL="postgresql+psycopg2://postgres:password@host.docker.internal:5432/movies_db" \
  -p 8000:8000 \
  shadoff6939/api-dru:dru
```

Replace `DB_URL` with your actual database connection string if needed.

### Use Existing Docker Image

You can also pull and run the prebuilt image directly from Docker Hub:

```bash
docker pull shadoff6939/api-dru2:dru

docker run \
  --env DB_URL=postgresql+psycopg2://test_user:password@localhost/test_db -p 8000:8000 <user-name>/<name-of-the-container>:<tag-name>
```

🔗 **Docker Hub**: [shadoff6939/api-dru2](https://hub.docker.com/r/shadoff6939/api-dru2)

---

Feel free to contribute, raise issues, or suggest improvements!
