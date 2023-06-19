from django_filters import rest_framework as filters

from Swipe.announcements.models import Announcement
from Swipe.residential_complexes.models import ResidentialComplex


class AnnouncementFilter(filters.FilterSet):
    min_price = filters.NumberFilter(field_name="price", lookup_expr='gte')
    max_price = filters.NumberFilter(field_name="price", lookup_expr='lte')
    min_area = filters.NumberFilter(field_name="area", lookup_expr='gte')
    max_area = filters.NumberFilter(field_name="area", lookup_expr='lte')
    microdistrict = filters.CharFilter(field_name='address', lookup_expr='contains')
    district = filters.CharFilter(field_name='address', lookup_expr='contains')
    house_status = filters.ChoiceFilter(field_name='residential_complex__house_status',
                                        choices=ResidentialComplex.HouseStatus.choices,
                                        method='filter_house_status')

    class Meta:
        model = Announcement
        fields = ['condition', 'payment_option', 'number_rooms', 'destination']

    def filter_house_status(self, queryset, name, value):
        return queryset.filter(residential_complex__house_status=value)
