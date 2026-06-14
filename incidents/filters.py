import django_filters
from .models import Incident


class IncidentFilter(django_filters.FilterSet):
    from_date = django_filters.DateFilter(field_name='created_at', lookup_expr='gte')
    to_date = django_filters.DateFilter(field_name='created_at', lookup_expr='lte')
    team = django_filters.CharFilter(field_name='assigned_team')

    class Meta:
        model = Incident
        fields = ['severity', 'status', 'team', 'from_date', 'to_date']
