import json
import time
import logging
from celery import shared_task
from django.conf import settings
from .models import Alert
from incidents.models import Incident
import anthropic

logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=3)
def classify_alert(self, alert_id):
    try:
        alert = Alert.objects.get(id=alert_id)
        if alert.processed:
            return

        client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)

        system_prompt = (
            "You are an incident classification engine. Respond only "
            "with valid JSON. No markdown, no explanation, no preamble."
        )

        user_prompt = (
            f"Classify this alert and respond with exactly this JSON structure:\n"
            f"{{\n"
            f"  'severity': 'P1|P2|P3|P4',\n"
            f"  'assigned_team': 'backend|frontend|devops|database',\n"
            f"  'suggested_action': 'string, 2-3 sentences max'\n"
            f"}}\n\n"
            f"Severity rules:\n"
            f"P1 = production down, data loss, security breach\n"
            f"P2 = major feature broken, significant user impact\n"
            f"P3 = minor feature degraded, workaround exists\n"
            f"P4 = cosmetic issue, no user impact\n\n"
            f"Alert details:\n"
            f"Service: {alert.service_name}\n"
            f"Environment: {alert.environment}\n"
            f"Error: {alert.error_message}"
        )

        start_time = time.time()

        try:
            response = client.messages.create(
                model="claude-haiku-4-5-20251001",
                max_tokens=300,
                system=system_prompt,
                messages=[
                    {"role": "user", "content": user_prompt}
                ]
            )
            response_text = response.content[0].text
        except Exception as e:
            logger.error(f"Claude API call failed: {str(e)}")
            raise self.retry(exc=e, countdown=5)

        end_time = time.time()
        latency_ms = int((end_time - start_time) * 1000)

        try:
            # Parse response, handling potential single quotes
            cleaned_text = response_text.replace("'", '"')
            data = json.loads(cleaned_text)
            severity = data.get('severity', 'P3')
            assigned_team = data.get('assigned_team', 'backend')
            suggested_action = data.get('suggested_action', '')

            # Basic validation
            if severity not in dict(Incident.SEVERITY_CHOICES):
                severity = 'P3'
            if assigned_team not in dict(Incident.TEAM_CHOICES):
                assigned_team = 'backend'

        except json.JSONDecodeError:
            severity = 'P3'
            assigned_team = 'backend'
            suggested_action = "Classification failed, manual review required"

        Incident.objects.create(
            alert=alert,
            severity=severity,
            assigned_team=assigned_team,
            suggested_action=suggested_action,
            classification_latency_ms=latency_ms
        )

        alert.processed = True
        alert.save()

    except Exception as e:
        logger.error(f"Task classify_alert failed for alert {alert_id}: {str(e)}")
        raise self.retry(exc=e, countdown=5)
