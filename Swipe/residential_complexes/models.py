from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from Swipe.users.models import User


class Advantage(models.Model):
    name = models.CharField(max_length=100, unique=True)
    logo = models.ImageField(upload_to='residential_complexes/advantages/')


# Create your models here.
class ResidentialComplex(models.Model):
    builder = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=150, unique=True)
    description = models.TextField()
    address = models.CharField(max_length=95, unique=True)
    advantages = models.ManyToManyField(Advantage)
    contact_first_name = models.CharField(max_length=50)
    contact_last_name = models.CharField(max_length=50)
    contact_phone = PhoneNumberField()

    class HouseStatus(models.TextChoices):
        APARTMENTS = 'apartments', 'Apartments'
        HOUSES = 'houses', 'Houses'

    class HouseType(models.TextChoices):
        MULTI_FAMILY = 'multiFamily', 'Multi-family'
        TOWNHOUSE = 'townhouse', 'Townhouse'
        CONDO = 'condo', 'Condo'
        SINGLE_FAMILY = 'singleFamily', 'Single-family'

    contact_email = models.EmailField()

    class HouseClass(models.TextChoices):
        ECONOMY = 'economy', 'Economy'
        COMFORT = 'comfort', 'Comfort'
        BUSINESS = 'business', 'Business'
        ELITE = 'elite', 'Elite'

    class ConstructionType(models.TextChoices):
        PRECAST_FOUNDATIONS = 'precastFoundations', 'Precast foundations'
        HYBRID_CONCRETE = 'hybridConcrete', 'Hybrid concrete'
        FLAT_SLABS = 'flatSlabs', 'Flat slabs'

    class TerritoryType(models.TextChoices):
        OPEN = 'open', 'Open'
        CLOSED = 'closed', 'Closed'
        CLOSED_PROTECTED = 'closedProtected', 'Closed and protected'

    house_status = models.CharField(max_length=10, choices=HouseStatus.choices)
    house_type = models.CharField(max_length=12, choices=HouseType.choices)
    house_class = models.CharField(max_length=8, choices=HouseClass.choices)
    construction = models.CharField(max_length=18, choices=ConstructionType.choices)
    territory = models.CharField(max_length=15, choices=TerritoryType.choices)
    distance_to_sea = models.SmallIntegerField()

    class CommunalPayment(models.TextChoices):
        PAYMENTS = 'payments', 'Payments'

    communal_payments = models.CharField(max_length=8, choices=CommunalPayment.choices)
    ceiling_height = models.FloatField()

    class UtilitiesType(models.TextChoices):
        WITHOUT = 'without', 'Without'
        CENTRAL = 'central', 'Central'

    gas = models.CharField(max_length=8, choices=UtilitiesType.choices)
    heating = models.CharField(max_length=8, choices=UtilitiesType.choices)
    sewerage = models.CharField(max_length=8, choices=UtilitiesType.choices)
    water_supply = models.CharField(max_length=8, choices=UtilitiesType.choices)


class News(models.Model):
    residential_complex = models.ForeignKey(ResidentialComplex, related_name='news', on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=64)
    text = models.TextField()


class Document(models.Model):
    residential_complex = models.ForeignKey(ResidentialComplex, related_name='documents', on_delete=models.CASCADE)
    is_excel = models.BooleanField(default=False)
    file = models.FileField(upload_to='residential_complexes/documents/')


class Image(models.Model):
    residential_complex = models.ForeignKey(ResidentialComplex, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='residential_complexes/images/')
    order = models.SmallIntegerField()

    class Meta:
        unique_together = ('residential_complex', 'order')


class Block(models.Model):
    residential_complex = models.ForeignKey(ResidentialComplex, related_name='blocks', on_delete=models.CASCADE)
    name = models.CharField(max_length=50)

    class Meta:
        unique_together = ('residential_complex', 'name')


class Section(models.Model):
    block = models.ForeignKey(Block, related_name='sections', on_delete=models.CASCADE)
    number = models.SmallIntegerField()

    class Meta:
        unique_together = ('block', 'number')


class Floor(models.Model):
    section = models.ForeignKey(Section, related_name='floors', on_delete=models.CASCADE)
    number = models.SmallIntegerField()

    class Meta:
        unique_together = ('section', 'number')


class Riser(models.Model):
    section = models.ForeignKey(Section, related_name='risers', on_delete=models.CASCADE)
    number = models.SmallIntegerField()

    class Meta:
        unique_together = ('section', 'number')