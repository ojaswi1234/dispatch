import uuid
from django.db import models
from alerts.models import Alert


class Incident(models.Model):
    SEVERITY_CHOICES = (
        ('P1', 'P1'),
        ('P2', 'P2'),
        ('P3', 'P3'),
        ('P4', 'P4'),
    )
    STATUS_CHOICES = (
        ('open', 'Open'),
        ('investigating', 'Investigating'),
        ('resolved', 'Resolved'),
    )
    TEAM_CHOICES = (
        ('backend', 'Backend'),
        ('frontend', 'Frontend'),
        ('devops', 'DevOps'),
        ('database', 'Database'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    alert = models.OneToOneField(Alert, on_delete=models.CASCADE)
    severity = models.CharField(max_length=2, choices=SEVERITY_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    assigned_team = models.CharField(max_length=20, choices=TEAM_CHOICES)
    suggested_action = models.TextField()
    classification_latency_ms = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    resolution_notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.severity} Incident - {self.status} - {self.id}"
