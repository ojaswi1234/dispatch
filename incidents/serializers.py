from rest_framework import serializers
from .models import Incident
from alerts.serializers import AlertSerializer


class IncidentSerializer(serializers.ModelSerializer):
    alert = AlertSerializer(read_only=True)

    class Meta:
        model = Incident
        fields = '__all__'
        read_only_fields = (
            'id', 'alert', 'severity', 'assigned_team', 'suggested_action',
            'classification_latency_ms', 'created_at', 'resolved_at'
        )


class IncidentResolveSerializer(serializers.Serializer):
    resolution_notes = serializers.CharField(required=True)
