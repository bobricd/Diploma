from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from Swipe.announcements.models import Announcement
from Swipe.residential_complexes.serializers import FloorSerializer, RiserSerializer


class ChessboardAnnouncementListSerializer(serializers.ModelSerializer):
    price_square_meter = serializers.SerializerMethodField()
    floor = FloorSerializer(read_only=True)
    riser = RiserSerializer(read_only=True)

    @extend_schema_field(OpenApiTypes.FLOAT)
    def get_price_square_meter(self, obj):
        if obj.area != 0:
            return round(obj.price / obj.area, 2)
        return None

    class Meta:
        model = Announcement
        fields = ('id', 'floor', 'riser', 'area', 'number_rooms', 'price', 'price_square_meter')

# class ChessboardSerializer(serializers.ModelSerializer):
#     block__residential_complex__announcements = AnnouncementListSerializer(many=True, read_only=True)
#
#     class Meta:
#         model = Section
#         fields = ('id', 'block__residential_complex__announcements')
