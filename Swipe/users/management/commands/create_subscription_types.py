from django.core.management.base import BaseCommand
from faker import Faker

from Swipe.users.models import SubscriptionType


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('number', type=int, help='how many subscription types generate')

    def handle(self, *args, **options):
        fake = Faker()
        for _ in range(options['number']):
            subscription_type = SubscriptionType.objects.create(
                name=fake.word(),
                price=fake.random_number(digits=2, fix_len=True)
            )
            print('Subscription type **' + subscription_type.name + '** successfully create')
