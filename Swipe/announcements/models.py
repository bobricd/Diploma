from django.db import models

from Swipe.promotions.models import PromotionType
from Swipe.residential_complexes.models import ResidentialComplex, Floor, Riser
from Swipe.users.models import User


# Create your models here.
class Announcement(models.Model):
    address = models.CharField(max_length=255)
    owner = models.ForeignKey(User, related_name='announcements', on_delete=models.CASCADE)
    residential_complex = models.ForeignKey(ResidentialComplex, related_name='announcements',
                                            null=True, on_delete=models.SET_NULL)

    class FoundationDocumentType(models.TextChoices):
        OWN = 'Own'

    class LayoutType(models.TextChoices):
        STUDIO = 'Studio'
        MICRO = 'Micro'
        LOFT = 'Loft'
        PENTHOUSE = 'Penthouse'

    class ConditionType(models.TextChoices):
        NEED_REPAIR = 'Need repair'
        GOOD = 'Good'
        BAD = 'Bad'

    class HeatingType(models.TextChoices):
        GAS = 'Gas'
        ELECTRICAL = 'Electrical'

    class PaymentType(models.TextChoices):
        CASH = 'Cash'
        CARD = 'Card'
        CRYPTOCURRENCY = 'Cryptocurrency'

    class AgentCommission(models.IntegerChoices):
        SMALL = 500
        MID = 1500
        BIG = 3000

    class CommunicationMethod(models.TextChoices):
        MESSAGES = 'Messages'
        PHONE = 'Phone'
        MESSAGE_PHONE = 'Message + phone'

    class ModerateIncorrectMessage(models.TextChoices):
        PHOTO = 'Incorrect photo'
        PRICE = 'Incorrect price'
        DESCRIPTION = 'Incorrect description'

    class DestinationType(models.TextChoices):
        APARTMENT = 'Apartment'
        HOUSE = 'House'

    foundation_document = models.CharField(max_length=3, choices=FoundationDocumentType.choices)
    destination = models.CharField(choices=DestinationType.choices, max_length=9)
    number_rooms = models.SmallIntegerField()
    layout = models.CharField(choices=LayoutType.choices, max_length=10)
    condition = models.CharField(choices=ConditionType.choices, max_length=11)
    area = models.SmallIntegerField()
    kitchen_area = models.SmallIntegerField()
    has_balcony = models.BooleanField()
    heating_type = models.CharField(choices=HeatingType.choices, max_length=11)
    payment_option = models.CharField(choices=PaymentType.choices, max_length=15)
    agent_commission = models.IntegerField(choices=AgentCommission.choices)
    communication_method = models.CharField(choices=CommunicationMethod.choices, max_length=15)
    description = models.TextField()
    price = models.IntegerField()
    is_moderate = models.BooleanField(default=False)
    approved = models.BooleanField(blank=True, null=True)
    moderate_message = models.CharField(choices=ModerateIncorrectMessage.choices, max_length=25)
    date_created = models.DateTimeField(auto_now_add=True)
    floor = models.ForeignKey(Floor, null=True, on_delete=models.SET_NULL)
    riser = models.ForeignKey(Riser, null=True, on_delete=models.SET_NULL)
    promotion_type = models.ForeignKey(PromotionType, null=True, on_delete=models.SET_NULL)

    class Meta:
        unique_together = ('floor', 'riser')
        ordering = ('-pk',)


class Image(models.Model):
    announcement = models.ForeignKey(Announcement, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='announcements/images/')


class Application(models.Model):
    residential_complex = models.ForeignKey(ResidentialComplex, related_name='applications', on_delete=models.CASCADE)
    announcement = models.ForeignKey(Announcement, related_name='applications', on_delete=models.CASCADE)
