from django.db import models


# Create your models here.
class PromotionType(models.Model):
    name = models.CharField(max_length=50, unique=True)
    price = models.FloatField()
    effectivity = models.SmallIntegerField()
