from django.urls import path
from .views import IncidentViewSet, IncidentStatsView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'', IncidentViewSet, basename='incident')

urlpatterns = [
    path('stats/', IncidentStatsView.as_view(), name='incident-stats'),
] + router.urls
