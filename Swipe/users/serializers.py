from dateutil.relativedelta import relativedelta
from dj_rest_auth.registration.serializers import RegisterSerializer
from django.utils import timezone
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers

from Swipe.announcements.serializers import AnnouncementListSerializer
from Swipe.residential_complexes.serializers import ResidentialComplexListSerializer
from Swipe.users.models import User, Message, Subscription, SubscriptionType


class FavouriteSerializer(serializers.ModelSerializer):
    favourite_residential_complex = ResidentialComplexListSerializer(many=True, read_only=True)
    favourite_announcements = AnnouncementListSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ('favourite_residential_complex', 'favourite_announcements')


class BuilderRegisterSerializer(RegisterSerializer):
    username = serializers.HiddenField(default=None, required=False)

    def validate_username(self, username):
        return None

    def custom_signup(self, request, user):
        user.role = User.RoleName.BUILDER
        user.save()


class OwnerRegisterSerializer(RegisterSerializer):
    username = serializers.HiddenField(default=None, required=False)

    def validate_username(self, username):
        return None

    def custom_signup(self, request, user):
        user.role = User.RoleName.OWNER
        user.save()


class BlackListSerializer(serializers.ModelSerializer):
    is_blocked = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'profile_image', 'first_name', 'last_name', 'phone',
                  'is_blocked', 'role'
                  ]

    def get_is_blocked(self, obj) -> bool:
        return obj.is_blocked


class UserSerializer(serializers.ModelSerializer):
    profile_image = serializers.ImageField(use_url=True)
    phone = PhoneNumberField()
    role = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'profile_image', 'first_name', 'last_name', 'phone',
                  'agent_first_name', 'agent_last_name', 'agent_phone', 'agent_email', 'switch_to_agent', 'role']


class MessageBaseSerializer(serializers.ModelSerializer):
    sender = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Message
        fields = '__all__'


class MessageListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'


class MessageAdminSerializer(MessageBaseSerializer):
    pass


class MessageUserSerializer(MessageBaseSerializer):
    receiver = serializers.HiddenField(default=User.objects.get(is_superuser=True))


class SubscriptionTypeSerializer(serializers.ModelSerializer):
    price = serializers.FloatField(min_value=0)

    class Meta:
        model = SubscriptionType
        fields = '__all__'


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'


class SubscriptionCreateSerializer(SubscriptionSerializer):
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())
    date = serializers.HiddenField(default=timezone.now().date() + relativedelta(months=1))

    def validate(self, attrs):
        if Subscription.objects.filter(owner=attrs.get('owner')).exists():
            raise serializers.ValidationError('Owner already have a subscription')
        else:
            return attrs


class SubscriptionUpdateSerializer(SubscriptionSerializer):
    class Meta:
        model = Subscription
        fields = ('date', 'subscription_type', 'auto_renewal')
