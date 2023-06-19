from django.db import models

from Swipe.announcements.models import Announcement
from Swipe.residential_complexes.models import ResidentialComplex
from Swipe.users.models import User


# Create your models here.
class SavedFilters(models.Model):
    user = models.ForeignKey(User, related_name='saved_filters', on_delete=models.CASCADE)
    min_price = models.SmallIntegerField(null=True)
    max_price = models.SmallIntegerField(null=True)
    min_area = models.SmallIntegerField(null=True)
    max_area = models.SmallIntegerField(null=True)
    microdistrict = models.CharField(max_length=50, null=True)
    district = models.CharField(max_length=50, null=True)
    house_status = models.CharField(max_length=10, choices=ResidentialComplex.HouseStatus.choices, null=True)
    condition = models.CharField(choices=Announcement.ConditionType.choices, max_length=11, null=True)
    payment_option = models.CharField(choices=Announcement.PaymentType.choices, max_length=15, null=True)
    number_rooms = models.SmallIntegerField(null=True)
    destination = models.CharField(choices=Announcement.DestinationType.choices, max_length=9, null=True)
