from drf_spectacular.utils import extend_schema
from rest_framework import permissions
from rest_framework.viewsets import ModelViewSet

from Swipe.saved_filters.models import SavedFilters
from Swipe.saved_filters.serializers import SavedFiltersSerializer


# Create your views here.
@extend_schema(tags=['Saved filters'])
class SavedFiltersViewSet(ModelViewSet):
    model = SavedFilters
    permission_classes = [permissions.IsAuthenticated]
    queryset = SavedFilters.objects.all()
    serializer_class = SavedFiltersSerializer
    http_method_names = ['get', 'post', "put", 'delete']

    def get_queryset(self):
        return SavedFilters.objects.filter(user=self.request.user)
