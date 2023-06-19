from allauth.account.views import ConfirmEmailView
from dj_rest_auth.registration.views import RegisterView
from django.db.models import Q
from django.db.models.deletion import ProtectedError
from django.shortcuts import redirect
from drf_psq import PsqMixin, Rule
from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.generics import ListAPIView, RetrieveUpdateAPIView, RetrieveAPIView
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from Swipe.users.models import User, Message, Subscription, SubscriptionType
from Swipe.users.permissions import IsOwner, IsBuilder, IsMessageSender, IsSubscriptionOwnerOrAdmin
from Swipe.users.serializers import BuilderRegisterSerializer, OwnerRegisterSerializer, \
    BlackListSerializer, UserSerializer, FavouriteSerializer, MessageAdminSerializer, MessageUserSerializer, \
    MessageListSerializer, SubscriptionSerializer, SubscriptionCreateSerializer, SubscriptionTypeSerializer


# Create your views here.

@extend_schema(tags=['Black List'])
class RemoveFromBlackListView(APIView):
    permission_classes = [permissions.IsAdminUser, permissions.IsAuthenticated]

    @extend_schema(responses={
        200: OpenApiResponse(
            description='User removed from black list.'),
        404: OpenApiResponse(description='User not found'),
    }, )
    def delete(self, request, pk):
        try:
            user = User.objects.get(id=pk)
            user.is_active = True
            user.save()
            return Response({'detail': f'{user.email} successfully remove from black list'},
                            status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)


@extend_schema(tags=['Black List'])
class AddToBlackListView(APIView):
    permission_classes = [permissions.IsAdminUser, permissions.IsAuthenticated]

    @extend_schema(request=None, responses={
        200: OpenApiResponse(description='User added to black list.'),
        404: OpenApiResponse(description='User not found'),
    }, )
    def post(self, request, pk):
        try:
            user = User.objects.get(id=pk)
            user.is_active = False
            user.save()
            return Response({'success': f'{user.email} successfully add to black list'},
                            status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)


@extend_schema(tags=['Favourites'])
class FavouriteListView(RetrieveAPIView):
    serializer_class = FavouriteSerializer
    permission_classes = [IsOwner, permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class CustomConfirmEmailView(ConfirmEmailView):
    def get(self, *args, **kwargs):
        self.object = confirmation = self.get_object()
        confirmation.confirm(self.request)
        if (
                self.request.user.is_authenticated
                and self.request.user.pk != confirmation.email_address.user_id
        ):
            self.logout()
        return redirect('rest_login')


class BuilderRegisterView(RegisterView):
    serializer_class = BuilderRegisterSerializer


class OwnerRegisterView(RegisterView):
    serializer_class = OwnerRegisterSerializer


@extend_schema(tags=['Black List'])
class BlackListView(ListAPIView):
    serializer_class = BlackListSerializer
    queryset = User.get_blocked_users()
    permission_classes = [permissions.IsAdminUser, permissions.IsAuthenticated]


class UserListView(ListAPIView):
    serializer_class = BlackListSerializer
    queryset = User.objects.all()
    permission_classes = [permissions.IsAdminUser, permissions.IsAuthenticated]


class UserDetailView(RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


@extend_schema(tags=['Subscription Types'])
class SubscriptionTypeViewSet(PsqMixin, viewsets.ModelViewSet):
    model = SubscriptionType
    queryset = SubscriptionType.objects.all()
    http_method_names = ['get', "put", 'post', 'delete']
    serializer_class = SubscriptionTypeSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        try:
            self.perform_destroy(instance)
        except ProtectedError:
            return Response(status=status.HTTP_423_LOCKED,
                            data={'detail': 'This subscription type cannot be deleted because'
                                            ' they have subscriptions associated with them.'})
        return Response(status=status.HTTP_204_NO_CONTENT)


@extend_schema(tags=['Subscriptions'])
class SubscriptionViewSet(PsqMixin, viewsets.ModelViewSet):
    model = Subscription
    queryset = Subscription.objects.all()
    http_method_names = ['get', "put", 'post', 'delete']
    serializer_class = SubscriptionSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]

    psq_rules = {
        'create': [
            Rule([permissions.IsAuthenticated, IsOwner], SubscriptionCreateSerializer)
        ],
        'retrieve': [
            Rule([IsSubscriptionOwnerOrAdmin])
        ]
    }

    @extend_schema(request=SubscriptionCreateSerializer)
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


@extend_schema(tags=['Messages'])
class MessageViewSet(PsqMixin, viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageAdminSerializer
    parser_classes = (MultiPartParser,)
    http_method_names = ['get', "put", 'post', 'delete']
    psq_rules = {
        'list': [
            Rule([permissions.IsAuthenticated], MessageListSerializer)
        ],
        'create': [
            Rule([permissions.IsAuthenticated, IsOwner | IsBuilder], MessageUserSerializer)
        ],
        'admin_create': [
            Rule([permissions.IsAuthenticated, permissions.IsAdminUser], MessageAdminSerializer)
        ],
        ('retrieve', 'update', 'partial_update', 'destroy'): [
            Rule([IsMessageSender, IsOwner | IsBuilder], MessageUserSerializer, get_obj=lambda self, obj: obj.sender),
            Rule([IsMessageSender, permissions.IsAdminUser], MessageAdminSerializer,
                 get_obj=lambda self, obj: obj.sender),
        ]
    }

    @extend_schema(request=None, responses=MessageListSerializer)
    def list(self, request, *args, **kwargs):
        self.queryset = Message.objects.filter(Q(sender=self.request.user) | Q(receiver=self.request.user))
        return super().list(request, *args, **kwargs)

    @extend_schema(request=MessageUserSerializer)
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(request=MessageAdminSerializer)
    @action(detail=False, methods=['post'])
    def admin_create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
