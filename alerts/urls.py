from django.urls import path
from .views import AlertIngestView, AlertViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'', AlertViewSet, basename='alert')

urlpatterns = [
    path('ingest/', AlertIngestView.as_view(), name='alert-ingest'),
] + router.urls
