from django.core.management.base import BaseCommand
from faker import Faker
from phonenumber_field.phonenumber import PhoneNumber

from Swipe.notaries.models import Notary


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('number', type=int, help='how many notaries generate')

    def handle(self, *args, **options):
        fake = Faker()
        for _ in range(options['number']):
            notary = Notary.objects.create(
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                phone=PhoneNumber.from_string('+38 (073) 485-59-99', region="UA"),
                email=fake.email()
            )
            print(f'Notary ** {notary.first_name} {notary.last_name} ** successfully create')
