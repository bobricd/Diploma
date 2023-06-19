from django.db import IntegrityError
from drf_psq import PsqMixin, Rule
from drf_spectacular.utils import extend_schema
from rest_framework import permissions, status, mixins
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from django_filters import rest_framework as filters

from Swipe.announcements.filters import AnnouncementFilter
from Swipe.announcements.models import Announcement, Application
from Swipe.announcements.serializers import AnnouncementCrateSerializer, AnnouncementDetailSerializer, \
    AnnouncementListSerializer, AnnouncementUpdateSerializer, AnnouncementModerateListSerializer, \
    AnnouncementModerateSerializer, ApplicationConfirmSerializer, \
    ApplicationSerializer, AnnouncementPromotionSerializer
from Swipe.users.permissions import IsOwner, IsAnnouncementOwner, IsBuilder, HaveResidentialComplex


class AnnouncementViewSet(PsqMixin, ModelViewSet):
    queryset = Announcement.objects.filter(approved=True)
    serializer_class = AnnouncementUpdateSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = AnnouncementFilter
    parser_classes = [MultiPartParser]
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['get', "put", 'post', 'delete']
    psq_rules = {
        'list': [
            Rule([permissions.IsAuthenticated], AnnouncementListSerializer)
        ],
        'announcement_my_list': [
            Rule([permissions.IsAuthenticated, IsAnnouncementOwner, IsOwner], AnnouncementListSerializer,
                 get_obj=lambda self, obj: obj.owner)
        ],
        'create': [
            Rule([permissions.IsAuthenticated, IsOwner], AnnouncementCrateSerializer)
        ],
        ('update', 'destroy', 'application_to_residential_complex', 'add_promotion'): [
            Rule([IsAnnouncementOwner, IsOwner], AnnouncementUpdateSerializer, get_obj=lambda self, obj: obj.owner)
        ],
        'to_residential_complex': [
            Rule([IsAnnouncementOwner, IsOwner], get_obj=lambda self, obj: obj.owner)
        ],
        'retrieve': [
            Rule([permissions.IsAuthenticated], AnnouncementDetailSerializer)
        ]
    }

    @extend_schema(responses=AnnouncementListSerializer)
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(request=AnnouncementCrateSerializer)
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(request=AnnouncementDetailSerializer)
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @action(detail=False, methods=['get'])
    def announcement_my_list(self, request, *args, **kwargs):
        self.queryset = Announcement.objects.filter(owner=request.user)
        return super().list(request, *args, **kwargs)

    # @action(detail=False, methods=['delete'], url_path='delete-image/(?P<pk>[^/.]+)')
    # def delete_image(self, request, pk=None):
    #     image = get_object_or_404(Image, pk=pk, announcement__in=request.user.announcements.all())
    #     image.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)

    @extend_schema(request=None)
    @action(detail=True, methods=['post'])
    def to_residential_complex(self, request, *args, **kwargs):
        announcement = self.get_object()
        if not Application.objects.filter(announcement=announcement).exists():
            try:
                Application.objects.create(announcement=announcement,
                                           residential_complex=announcement.residential_complex)
            except IntegrityError:
                return Response({'success': "Application doesn't have residential complex"},
                                status=status.HTTP_400_BAD_REQUEST)
            return Response({'success': 'Application successfully created'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Application with this announcement already exists'},
                            status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(request=None)
    @extend_schema(tags=['Announcement favourites'])
    @action(detail=False, methods=['post'], url_path='add-to-favourite/(?P<pk>[^/.]+)')
    def add_to_favourite(self, request, pk=None):
        user = request.user
        try:
            announcement = Announcement.objects.get(id=pk)
            user.favourite_announcements.add(announcement)
            return Response({'success': 'Announcement successfully add to favourite'},
                            status=status.HTTP_200_OK)
        except Announcement.DoesNotExist:
            return Response({'error': 'Announcement not found'}, status=status.HTTP_404_NOT_FOUND)

    @extend_schema(request=None)
    @extend_schema(tags=['Announcement favourites'])
    @action(detail=False, methods=['delete'], url_path='remove-from-favourite/(?P<pk>[^/.]+)')
    def remove_from_favourite(self, request, pk=None):
        user = request.user
        try:
            announcement = Announcement.objects.get(id=pk)
            user.favourite_announcements.remove(announcement)
            return Response({'success': 'Announcement successfully removed from favourite'},
                            status=status.HTTP_204_NO_CONTENT)
        except Announcement.DoesNotExist:
            return Response({'error': 'Announcement not found'}, status=status.HTTP_404_NOT_FOUND)

    @extend_schema(request=AnnouncementPromotionSerializer)
    @extend_schema(tags=['Announcement promotion'])
    @action(detail=True, methods=['put'])
    def set_promotion(self, request, pk=None):
        instance = self.get_object()
        serializer = AnnouncementPromotionSerializer(instance=instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}
        return Response(serializer.data)


@extend_schema(tags=['announcement-moderation'])
class AnnouncementModerateViewSet(PsqMixin,
                                  mixins.ListModelMixin,
                                  mixins.RetrieveModelMixin,
                                  mixins.UpdateModelMixin,
                                  GenericViewSet):
    queryset = Announcement.objects.filter(is_moderate=False)
    serializer_class = AnnouncementModerateSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    http_method_names = ['get', "put"]
    psq_rules = {
        'list': [
            Rule([permissions.IsAuthenticated, permissions.IsAdminUser],
                 serializer_class=AnnouncementModerateListSerializer)
        ]
    }

    @extend_schema(responses=AnnouncementModerateListSerializer)
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


@extend_schema(tags=['Applications'])
class ApplicationsViewSet(PsqMixin, ModelViewSet):
    model = Application
    queryset = Application.objects.none()
    http_method_names = ['get', "put", 'delete']
    serializer_class = ApplicationSerializer
    permission_classes = [permissions.IsAuthenticated, HaveResidentialComplex, IsBuilder]
    psq_rules = {
        'update': [
            Rule([permissions.IsAuthenticated, HaveResidentialComplex, IsBuilder], ApplicationConfirmSerializer)
        ],
    }

    def get_queryset(self):
        return Application.objects.filter(residential_complex=self.request.user.residentialcomplex)

    @extend_schema(request=ApplicationConfirmSerializer)
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance.announcement, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}
        self.perform_destroy(instance)
        return Response(serializer.data)