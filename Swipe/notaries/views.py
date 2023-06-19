from django.shortcuts import render
from drf_psq import PsqMixin, Rule
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, permissions

from Swipe.notaries.models import Notary
from Swipe.notaries.serializers import NotarySerializer


# Create your views here.
class NotaryViewSet(PsqMixin, viewsets.ModelViewSet):
    queryset = Notary.objects.all()
    serializer_class = NotarySerializer
    permission_classes = [permissions.IsAdminUser, permissions.IsAuthenticated]
    http_method_names = ['get', "put", 'post', 'delete']
    psq_rules = {
        'list': [
            Rule([permissions.IsAuthenticated])
        ],
    }
