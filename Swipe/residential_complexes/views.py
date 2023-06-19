from django.shortcuts import get_object_or_404
from drf_psq import PsqMixin, Rule
from drf_spectacular.utils import extend_schema
from rest_framework import permissions, status
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from Swipe.residential_complexes.models import ResidentialComplex, Document, Advantage, Block, Section, Floor, Riser
from Swipe.residential_complexes.serializers import ResidentialComplexListSerializer,\
    ResidentialComplexCreateSerializer, ResidentialComplexUpdateSerializer, DocumentSerializer, NewsSerializer, \
    AdvantageSerializer, BlockSerializer, SectionSerializer, FloorSerializer, RiserSerializer
from Swipe.users.permissions import IsBuilder, IsOwner, HaveResidentialComplex


# Create your views here.


class ResidentialComplexListView(ListAPIView):
    queryset = ResidentialComplex.objects.all()
    serializer_class = ResidentialComplexListSerializer
    permission_classes = [permissions.IsAuthenticated]


class ResidentialComplexCreateView(CreateAPIView):
    serializer_class = ResidentialComplexCreateSerializer
    permission_classes = [permissions.IsAuthenticated, IsBuilder]


class ResidentialComplexDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = ResidentialComplexUpdateSerializer
    queryset = ResidentialComplex.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsBuilder]
    http_method_names = ['get', "put", 'delete']

    def get_object(self):
        residential_complex = get_object_or_404(ResidentialComplex, builder=self.request.user)
        self.check_object_permissions(self.request, residential_complex)
        return residential_complex


@extend_schema(tags=['Residential complex favourites'])
class AddFavouriteResidentialComplexView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    @extend_schema(request=None, responses=None)
    def post(self, request, pk):
        user = request.user
        try:
            residential_complex = ResidentialComplex.objects.get(id=pk)
            user.favourite_residential_complex.add(residential_complex)
            return Response({'success': 'ResidentialComplex successfully add to favourite'},
                            status=status.HTTP_200_OK)
        except ResidentialComplex.DoesNotExist:
            return Response({'error': 'ResidentialComplex not found'}, status=status.HTTP_404_NOT_FOUND)


@extend_schema(tags=['Residential complex favourites'])
class RemoveFavouriteResidentialComplexView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    @extend_schema(request=None, responses=None)
    def delete(self, request, pk):
        user = request.user
        try:
            residential_complex = ResidentialComplex.objects.get(id=pk)
            user.favourite_residential_complex.remove(residential_complex)
            return Response({'success': 'ResidentialComplex successfully removed from favourite'},
                            status=status.HTTP_204_NO_CONTENT)
        except ResidentialComplex.DoesNotExist:
            return Response({'error': 'ResidentialComplex not found'}, status=status.HTTP_404_NOT_FOUND)


class DocumentCreateView(CreateAPIView):
    parser_classes = [MultiPartParser]
    serializer_class = DocumentSerializer
    queryset = Document.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsBuilder]


class NewsCreateView(CreateAPIView):
    serializer_class = NewsSerializer
    permission_classes = [permissions.IsAuthenticated, IsBuilder]


@extend_schema(tags=['Advantages'])
class AdvantageViewSet(PsqMixin, ModelViewSet):
    parser_classes = [MultiPartParser]
    queryset = Advantage.objects.all()
    serializer_class = AdvantageSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    http_method_names = ['get', "put", 'post', 'delete']
    psq_rules = {
        'list': [
            Rule([permissions.IsAuthenticated, permissions.IsAdminUser | IsBuilder])
        ]
    }


@extend_schema(tags=['Blocks'])
class BlockViewSet(PsqMixin, ModelViewSet):
    queryset = Block.objects.none()
    model = Block
    serializer_class = BlockSerializer
    permission_classes = [permissions.IsAuthenticated, HaveResidentialComplex, IsBuilder]
    http_method_names = ['get', "put", 'post', 'delete']

    def get_queryset(self):
        queryset = Block.objects.filter(residential_complex=self.request.user.residentialcomplex)
        return queryset


@extend_schema(tags=['Sections'])
class SectionViewSet(PsqMixin, ModelViewSet):
    queryset = Section.objects.none()
    model = Section
    serializer_class = SectionSerializer
    permission_classes = [permissions.IsAuthenticated, HaveResidentialComplex, IsBuilder]
    http_method_names = ['get', "put", 'post', 'delete']

    def get_queryset(self):
        queryset = Section.objects.filter(block__residential_complex=self.request.user.residentialcomplex)
        return queryset


@extend_schema(tags=['Floors'])
class FloorViewSet(PsqMixin, ModelViewSet):
    queryset = Floor.objects.none()
    model = Floor
    serializer_class = FloorSerializer
    permission_classes = [permissions.IsAuthenticated, HaveResidentialComplex, IsBuilder]
    http_method_names = ['get', "put", 'post', 'delete']

    def get_queryset(self):
        queryset = Floor.objects.filter(section__block__residential_complex=self.request.user.residentialcomplex)
        return queryset


@extend_schema(tags=['Risers'])
class RiserViewSet(PsqMixin, ModelViewSet):
    queryset = Riser.objects.none()
    model = Riser
    serializer_class = RiserSerializer
    permission_classes = [permissions.IsAuthenticated, HaveResidentialComplex, IsBuilder]
    http_method_names = ['get', "put", 'post', 'delete']

    def get_queryset(self):
        queryset = Riser.objects.filter(section__block__residential_complex=self.request.user.residentialcomplex)
        return queryset
#
