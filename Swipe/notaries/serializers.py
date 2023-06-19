from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers

from Swipe.notaries.models import Notary


class NotarySerializer(serializers.ModelSerializer):
    phone = PhoneNumberField()

    class Meta:
        model = Notary
        fields = '__all__'
