import uuid
from django.db import models


class Alert(models.Model):
    ENVIRONMENT_CHOICES = (
        ('production', 'Production'),
        ('staging', 'Staging'),
        ('development', 'Development'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    service_name = models.CharField(max_length=100)
    environment = models.CharField(max_length=50, choices=ENVIRONMENT_CHOICES)
    error_message = models.TextField()
    payload = models.JSONField()
    received_at = models.DateTimeField(auto_now_add=True)
    processed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.service_name} ({self.environment}) - {self.id}"
