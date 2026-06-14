import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from django.contrib.auth.models import User
from alerts.models import Alert
from incidents.models import Incident
from django.utils import timezone

pytestmark = pytest.mark.django_db


@pytest.fixture
def auth_client():
    user = User.objects.create_user(username='testuser', password='testpassword')
    client = APIClient()
    client.force_authenticate(user=user)
    return client


@pytest.fixture
def setup_incidents():
    a1 = Alert.objects.create(
        service_name="S1", environment="production", error_message="E1", payload={}
    )
    a2 = Alert.objects.create(
        service_name="S2", environment="production", error_message="E2", payload={}
    )
    i1 = Incident.objects.create(
        alert=a1, severity="P1", status="open", assigned_team="backend",
        suggested_action="A1", classification_latency_ms=100
    )
    i2 = Incident.objects.create(
        alert=a2, severity="P3", status="resolved", assigned_team="frontend",
        suggested_action="A2", classification_latency_ms=200, resolved_at=timezone.now()
    )
    return [i1, i2]


def test_list_incidents_filter_by_severity(auth_client, setup_incidents):
    url = reverse('incident-list')
    response = auth_client.get(f"{url}?severity=P1")
    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]['severity'] == 'P1'


def test_list_incidents_filter_by_status(auth_client, setup_incidents):
    url = reverse('incident-list')
    response = auth_client.get(f"{url}?status=resolved")
    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]['status'] == 'resolved'


def test_resolve_incident_sets_resolved_at(auth_client, setup_incidents):
    i1 = setup_incidents[0]
    url = reverse('incident-resolve', args=[i1.id])
    response = auth_client.patch(url, {'resolution_notes': 'Fixed the bug'}, format='json')
    assert response.status_code == 200
    i1.refresh_from_db()
    assert i1.status == 'resolved'
    assert i1.resolved_at is not None
    assert i1.resolution_notes == 'Fixed the bug'


def test_resolve_incident_requires_resolution_notes(auth_client, setup_incidents):
    i1 = setup_incidents[0]
    url = reverse('incident-resolve', args=[i1.id])
    response = auth_client.patch(url, {}, format='json')
    assert response.status_code == 400
