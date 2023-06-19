from django.db.models import F, Q
from django_filters import rest_framework as filters

from Swipe.announcements.models import Announcement
from Swipe.residential_complexes.models import ResidentialComplex


class ChessboardFilter(filters.FilterSet):
    min_price = filters.NumberFilter(field_name="price", lookup_expr='gte')
    max_price = filters.NumberFilter(field_name="price", lookup_expr='lte')
    min_area = filters.NumberFilter(field_name="area", lookup_expr='gte')
    max_area = filters.NumberFilter(field_name="area", lookup_expr='lte')
    min_price_square_meter = filters.NumberFilter(method='filter_price_square_meter_gte')
    max_price_square_meter = filters.NumberFilter(method='filter_price_square_meter_lte')

    class Meta:
        model = Announcement
        fields = ['condition', 'payment_option', 'number_rooms']

    def filter_price_square_meter_gte(self, queryset, name, value):
        return queryset.annotate(price_square_meter=F('price') / F('area')).filter(price_square_meter__gte=value)

    def filter_price_square_meter_lte(self, queryset, name, value):
        return queryset.annotate(price_square_meter=F('price') / F('area')).filter(price_square_meter__lte=value)
