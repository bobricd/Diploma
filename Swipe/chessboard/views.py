from drf_spectacular.utils import extend_schema
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from Swipe.announcements.models import Announcement
from Swipe.chessboard.filters import ChessboardFilter
from Swipe.chessboard.serializers import ChessboardAnnouncementListSerializer
from django_filters import rest_framework as filters
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter

# Create your views here.
@extend_schema(tags=['Chessboard'])
class ChessboardViewSet(GenericViewSet):
    queryset = Announcement.objects.none()
    serializer_class = ChessboardAnnouncementListSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = ChessboardFilter
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Announcement.objects.filter(floor__isnull=False, riser__isnull=False,
                                           residential_complex=self.request.user.residentialcomplex)

    @extend_schema(
        parameters=[
            OpenApiParameter('min_price', OpenApiTypes.NUMBER, OpenApiParameter.QUERY),
            OpenApiParameter('max_price', OpenApiTypes.NUMBER, OpenApiParameter.QUERY),
            OpenApiParameter('min_area', OpenApiTypes.NUMBER, OpenApiParameter.QUERY),
            OpenApiParameter('max_area', OpenApiTypes.NUMBER, OpenApiParameter.QUERY),
            OpenApiParameter('min_price_square_meter', OpenApiTypes.NUMBER, OpenApiParameter.QUERY),
            OpenApiParameter('max_price_square_meter', OpenApiTypes.NUMBER, OpenApiParameter.QUERY),
        ], description='<b>The {id} parameter in the link must be filled with the Section_id</b>')
    @action(detail=False, methods=['get'], url_path='chessboard-list/(?P<pk>[^/.]+)')
    def chessboard_list(self, request, pk=None):
        queryset = self.filter_queryset(self.get_queryset().filter(floor__section=pk).order_by('floor', 'riser'))
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


    @action(detail=False, methods=['get'], url_path='chessboard-announcement/(?P<pk>[^/.]+)')
    def chessboard_announcement_detail(self, request, pk=None):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

