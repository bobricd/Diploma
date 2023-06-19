from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


# Create your models here.
class Notary(models.Model):
    first_name = models.CharField(blank=True, max_length=50)
    last_name = models.CharField(blank=True, max_length=50)
    phone = PhoneNumberField(blank=True)
    email = models.EmailField(unique=True)
