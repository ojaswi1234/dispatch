from rest_framework import serializers
from .models import Alert


class AlertSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alert
        fields = '__all__'
        read_only_fields = ('id', 'received_at', 'processed')


class AlertIngestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alert
        fields = ('service_name', 'environment', 'error_message', 'payload')
