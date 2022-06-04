from django_filters import rest_framework as filters
from advertisements.models import Advertisement


class AdvertisementFilter(filters.FilterSet):
    created_at_before = filters.DateFilter( field_name='created_at', lookup_expr='date__lte')

    class Meta:
        model = Advertisement
        fields = ['creator', 'created_at', 'status']
