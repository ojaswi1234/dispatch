# Dispatch - Incident Management API

Production-quality Django REST Framework incident management API with Celery and Claude LLM classification.

## Local Setup

### 1. Clone and create virtual environment
```bash
git clone <repo-url>
cd dispatch
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Install requirements
```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

### 3. Set up .env
```bash
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY
```

### 4. Docker Compose
Run the full stack (Django, PostgreSQL, Redis, Celery):
```bash
docker-compose up --build
```

### 5. Run migrations (inside the web container)
```bash
docker-compose exec web python manage.py migrate
```

### 6. Create superuser
```bash
docker-compose exec web python manage.py createsuperuser
```

### 7. Run tests
```bash
# Run locally (requires Postgres and Redis running or mocked)
pytest

# Or run inside the container
docker-compose exec web pytest
```

### 8. API Documentation
Hit the Swagger docs URL:
[http://localhost:8000/api/docs/](http://localhost:8000/api/docs/)

## Architecture
- **Alert Ingest**: Open endpoint for system webhooks.
- **Classification**: Async task via Celery using Claude Haiku.
- **Incidents**: JWT-protected endpoints for management and stats.
- **CI/CD**: GitHub Actions pipeline for linting, testing, and Docker build.
