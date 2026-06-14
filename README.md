# Dispatch - AI-Powered Incident Management

Dispatch is a production-quality Incident Management API built with **Django REST Framework**. It automates the process of receiving system alerts, classifying their severity using **Claude AI**, and routing them to the appropriate engineering teams.

## 🚀 What does it do?

1.  **Alert Ingestion**: Provides a high-throughput endpoint to receive webhooks and alerts from external monitoring tools (e.g., Grafana, Datadog, Sentry).
2.  **AI Classification**: Automatically analyzes incoming alerts using **Claude LLM** to determine:
    *   **Severity**: (P1 to P4) based on the impact described.
    *   **Routing**: Assigns the incident to the correct team (Backend, Frontend, DevOps, or Database).
    *   **Actionable Advice**: Generates immediate suggested actions for responders.
3.  **Incident Lifecycle**: Tracks incidents from 'Open' to 'Resolved', providing an audit trail of how alerts were handled.
4.  **Analytics**: Tracks classification latency and incident statistics to monitor system health and team response times.

## 🛠 Tech Stack

*   **Backend**: Python / Django / Django REST Framework
*   **Database**: PostgreSQL
*   **Task Queue**: Celery with Redis (for async AI classification)
*   **AI Engine**: Claude API (Anthropic)
*   **Infrastructure**: Docker & Docker Compose
*   **Testing**: Pytest

## 📖 How it works

1.  **Ingest**: An external system sends a POST request to `/api/alerts/ingest/`.
2.  **Queue**: The alert is saved to the database, and a background task is dispatched to Celery.
3.  **Classify**: Celery calls the Claude API. The LLM evaluates the error message and environment to create a structured classification.
4.  **Incident**: A new `Incident` record is created, linked to the alert, and ready for the engineering team to review.

---

## 🚦 Getting Started

### 1. Prerequisites
*   Docker and Docker Compose
*   Python 3.12+ (for local development)
*   An [Anthropic API Key](https://console.anthropic.com/)

### 2. Environment Setup
Copy the example environment file and add your Anthropic key:
```bash
cp .env.example .env
# Edit .env and set ANTHROPIC_API_KEY=your_key_here
```

### 3. Spin up the Infrastructure
Start PostgreSQL and Redis:
```bash
docker-compose up -d db redis
```

### 4. Application Setup
Install dependencies and run migrations:
```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
```

### 5. Run the Services
You need two terminals running to have the full system operational:

**Terminal 1 (Web Server):**
```bash
python manage.py runserver
```

**Terminal 2 (AI Worker):**
```bash
celery -A dispatch worker --loglevel=info
```

---

## 📋 API Reference

| Endpoint | Method | Description | Auth |
| :--- | :--- | :--- | :--- |
| `/api/docs/` | GET | Interactive Swagger Documentation | None |
| `/api/alerts/ingest/` | POST | Ingest a new system alert | None |
| `/api/incidents/` | GET | List all active incidents | JWT |
| `/api/incidents/stats/` | GET | View incident statistics | JWT |
| `/api/auth/token/` | POST | Obtain JWT Access/Refresh tokens | Credentials |

**Example Alert Payload:**
```json
{
  "service_name": "payment-gateway",
  "environment": "production",
  "error_message": "Database connection timeout in checkout flow",
  "payload": {"stack_trace": "..."}
}
```

---

## 🧪 Testing
Run the test suite locally:
```bash
pytest
```
