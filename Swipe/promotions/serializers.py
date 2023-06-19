from rest_framework import serializers

from Swipe.promotions.models import PromotionType


class PromotionTypeSerializer(serializers.ModelSerializer):
    effectivity = serializers.FloatField(max_value=100)

    class Meta:
        model = PromotionType
        fields = '__all__'

# class AnnouncementPromotionSerializer()