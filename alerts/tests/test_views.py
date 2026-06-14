import pytest
from unittest import mock
from rest_framework.test import APIClient
from django.urls import reverse
from alerts.models import Alert
from django.contrib.auth.models import User

pytestmark = pytest.mark.django_db


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def auth_client():
    user = User.objects.create_user(username='testuser', password='testpassword')
    client = APIClient()
    client.force_authenticate(user=user)
    return client


@mock.patch('alerts.tasks.classify_alert.delay')
def test_ingest_no_auth_required(mock_delay, api_client):
    url = reverse('alert-ingest')
    payload = {
        "service_name": "payment-api",
        "environment": "production",
        "error_message": "Timeout connecting to gateway",
        "payload": {"raw": "data"}
    }
    response = api_client.post(url, payload, format='json')
    assert response.status_code == 202


def test_ingest_missing_fields_returns_400(api_client):
    url = reverse('alert-ingest')
    payload = {
        "environment": "production",
        "error_message": "Missing service_name",
        "payload": {}
    }
    response = api_client.post(url, payload, format='json')
    assert response.status_code == 400


@mock.patch('alerts.tasks.classify_alert.delay')
def test_ingest_creates_alert_record(mock_delay, api_client):
    url = reverse('alert-ingest')
    payload = {
        "service_name": "auth-service",
        "environment": "staging",
        "error_message": "JWT validation failed",
        "payload": {"key": "value"}
    }
    api_client.post(url, payload, format='json')
    assert Alert.objects.filter(service_name="auth-service").exists()


def test_list_alerts_requires_jwt(api_client):
    url = reverse('alert-list')
    response = api_client.get(url)
    assert response.status_code == 401
