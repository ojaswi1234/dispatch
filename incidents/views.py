from django.utils import timezone
from django.db.models import Count, Avg, F
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema
from .models import Incident
from .serializers import IncidentSerializer, IncidentResolveSerializer
from .filters import IncidentFilter


class IncidentViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Incident.objects.all().order_by('-created_at')
    serializer_class = IncidentSerializer
    permission_classes = [IsAuthenticated]
    filterset_class = IncidentFilter

    @extend_schema(summary="List all incidents")
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(summary="Retrieve a specific incident")
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        request=IncidentResolveSerializer,
        responses={200: IncidentSerializer},
        summary="Resolve an incident"
    )
    @action(detail=True, methods=['patch'])
    def resolve(self, request, pk=None):
        incident = self.get_object()
        serializer = IncidentResolveSerializer(data=request.data)
        if serializer.is_valid():
            incident.status = 'resolved'
            incident.resolved_at = timezone.now()
            incident.resolution_notes = serializer.validated_data['resolution_notes']
            incident.save()
            return Response(IncidentSerializer(incident).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class IncidentStatsView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(summary="Get incident statistics")
    def get(self, request):
        incidents = Incident.objects.all()

        total = incidents.count()

        severity_breakdown = list(incidents.values('severity').annotate(count=Count('id')))
        status_breakdown = list(incidents.values('status').annotate(count=Count('id')))

        avg_latency = incidents.aggregate(avg=Avg('classification_latency_ms'))['avg']

        resolved_incidents = incidents.filter(status='resolved', resolved_at__isnull=False)
        # Calculate resolution time in minutes
        avg_resolution_time = None
        if resolved_incidents.exists():
            avg_res_timedelta = resolved_incidents.annotate(
                duration=F('resolved_at') - F('created_at')
            ).aggregate(avg_duration=Avg('duration'))['avg_duration']
            if avg_res_timedelta:
                avg_resolution_time = avg_res_timedelta.total_seconds() / 60.0

        return Response({
            'total_incidents': total,
            'breakdown_by_severity': severity_breakdown,
            'breakdown_by_status': status_breakdown,
            'average_classification_latency_ms': avg_latency or 0,
            'average_resolution_time_minutes': avg_resolution_time
        })
