import pytest
from unittest import mock
from alerts.models import Alert
from incidents.models import Incident
from alerts.tasks import classify_alert

pytestmark = pytest.mark.django_db


class MockMessage:
    def __init__(self, text):
        self.text = text


class MockResponse:
    def __init__(self, text):
        self.content = [MockMessage(text)]


@mock.patch('anthropic.resources.messages.Messages.create')
def test_classify_alert_creates_incident(mock_create):
    mock_llm_response = '''
    {
        "severity": "P1",
        "assigned_team": "backend",
        "suggested_action": "Restart the service"
    }
    '''
    mock_create.return_value = MockResponse(mock_llm_response)

    alert = Alert.objects.create(
        service_name="test-service",
        environment="production",
        error_message="test error",
        payload={}
    )

    classify_alert(alert.id)

    incident = Incident.objects.get(alert=alert)
    assert incident.severity == 'P1'
    assert incident.assigned_team == 'backend'
    assert incident.suggested_action == 'Restart the service'
    assert incident.classification_latency_ms >= 0

    alert.refresh_from_db()
    assert alert.processed is True


@mock.patch('anthropic.resources.messages.Messages.create')
def test_classify_alert_handles_bad_llm_response(mock_create):
    mock_bad_llm_response = 'not valid json'
    mock_create.return_value = MockResponse(mock_bad_llm_response)

    alert = Alert.objects.create(
        service_name="test-service",
        environment="production",
        error_message="test error",
        payload={}
    )

    classify_alert(alert.id)

    incident = Incident.objects.get(alert=alert)
    assert incident.severity == 'P3'
    assert incident.assigned_team == 'backend'
    assert incident.suggested_action == 'Classification failed, manual review required'

    alert.refresh_from_db()
    assert alert.processed is True
