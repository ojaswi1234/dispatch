import logging
from rest_framework import status, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from drf_spectacular.utils import extend_schema, OpenApiResponse
from .models import Alert
from .serializers import AlertSerializer, AlertIngestSerializer
from .tasks import classify_alert

logger = logging.getLogger(__name__)


class AlertIngestView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        request=AlertIngestSerializer,
        responses={202: OpenApiResponse(description="Alert accepted for processing")},
        summary="Ingest a new alert"
    )
    def post(self, request):
        serializer = AlertIngestSerializer(data=request.data)
        if serializer.is_valid():
            alert = serializer.save()
            classify_alert.delay(alert.id)
            return Response({'id': alert.id}, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AlertViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Alert.objects.all().order_by('-received_at')
    serializer_class = AlertSerializer
    permission_classes = [IsAuthenticated]

    @extend_schema(summary="List all alerts")
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(summary="Retrieve a specific alert")
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
