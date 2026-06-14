import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from django.contrib.auth.models import User
from alerts.models import Alert
from incidents.models import Incident

pytestmark = pytest.mark.django_db


@pytest.fixture
def auth_client():
    user = User.objects.create_user(username='testuser', password='testpassword')
    client = APIClient()
    client.force_authenticate(user=user)
    return client


def test_stats_endpoint_returns_correct_structure(auth_client):
    a1 = Alert.objects.create(
        service_name="S1", environment="production", error_message="E1", payload={}
    )
    Incident.objects.create(
        alert=a1, severity="P1", status="open", assigned_team="backend",
        suggested_action="A1", classification_latency_ms=100
    )

    url = reverse('incident-stats')
    response = auth_client.get(url)
    assert response.status_code == 200

    data = response.data
    assert 'total_incidents' in data
    assert 'breakdown_by_severity' in data
    assert 'breakdown_by_status' in data
    assert 'average_classification_latency_ms' in data
    assert 'average_resolution_time_minutes' in data
    assert data['total_incidents'] == 1
