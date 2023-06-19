from allauth.account.models import EmailAddress
from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from .managers import CustomUserManager


# Create your models here.

class User(AbstractUser):
    class RoleName(models.TextChoices):
        OWNER = ('owner', 'owner')
        BUILDER = ('builder', 'builder')

    username = None
    email = models.EmailField(unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()
    role = models.CharField(max_length=7, choices=RoleName.choices)
    profile_image = models.ImageField(upload_to='users')
    first_name = models.CharField(blank=True, max_length=50)
    last_name = models.CharField(blank=True, max_length=50)
    phone = PhoneNumberField(blank=True)
    # Agent info
    agent_first_name = models.CharField(blank=True, max_length=50)
    agent_last_name = models.CharField(blank=True, max_length=50)
    agent_phone = PhoneNumberField(blank=True)
    agent_email = models.EmailField(blank=True)
    switch_to_agent = models.BooleanField(default=False)

    # Favourites
    favourite_announcements = models.ManyToManyField("announcements.Announcement")
    favourite_residential_complex = models.ManyToManyField(
        "residential_complexes.ResidentialComplex")

    # saved_filters = models.ManyToManyField()

    @staticmethod
    def get_blocked_users():
        email_address = EmailAddress.objects.filter(verified=True).values('email')
        return User.objects.filter(is_active=False, email__in=email_address)

    @property
    def is_blocked(self):
        try:
            if EmailAddress.objects.get(user_id=self.pk).verified and not self.is_active:
                return True
        except EmailAddress.DoesNotExist:
            pass
        return False

    def __str__(self):
        return self.email


class Message(models.Model):
    sender = models.ForeignKey(User, related_name='senders', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='receivers', on_delete=models.CASCADE)
    text = models.TextField()
    file = models.FileField(upload_to='messages/files/', blank=True, null=True)

    class Meta:
        ordering = ['sender', 'receiver', 'id']


class SubscriptionType(models.Model):
    name = models.CharField(max_length=50, unique=True)
    price = models.FloatField()


class Subscription(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    date = models.DateField()
    subscription_type = models.ForeignKey(SubscriptionType, on_delete=models.PROTECT)
    auto_renewal = models.BooleanField(default=True)
