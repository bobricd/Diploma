from rest_framework import serializers

from Swipe.saved_filters.models import SavedFilters


class SavedFiltersSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = SavedFilters
        fields = '__all__'
