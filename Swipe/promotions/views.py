from django.shortcuts import render
from drf_psq import PsqMixin, Rule
from drf_spectacular.utils import extend_schema
from rest_framework import permissions
from rest_framework.viewsets import ModelViewSet

from Swipe.promotions.models import PromotionType
from Swipe.promotions.serializers import PromotionTypeSerializer


# Create your views here.
@extend_schema(tags=['Promotion types'])
class PromotionTypeViewSet(PsqMixin, ModelViewSet):
    model = PromotionType
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    queryset = PromotionType.objects.all()
    serializer_class = PromotionTypeSerializer
    http_method_names = ['get', 'post', "put", 'delete']
    psq_rules = {
        'list': [
            Rule([permissions.IsAuthenticated])
        ],
    }
