import random
from django.core.management.base import BaseCommand
from faker import Faker

from Swipe.promotions.models import PromotionType


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('number', type=int, help='how many promotion types generate')

    def handle(self, *args, **options):
        fake = Faker()
        for _ in range(options['number']):
            promotion_type = PromotionType.objects.create(
                name=fake.word(),
                price=random.randrange(1, 200),
                effectivity=random.randrange(1, 100)
            )
            print(f'Promotion Type ** {promotion_type.name} ** successfully create')
