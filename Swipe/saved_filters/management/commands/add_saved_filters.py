from django.core.management.base import BaseCommand
from faker import Faker

from Swipe.announcements.models import Announcement
from Swipe.residential_complexes.models import ResidentialComplex
from Swipe.saved_filters.models import SavedFilters
from Swipe.users.models import User


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('number', type=int, help='how many saved filters generate how each user')

    def handle(self, *args, **options):
        fake = Faker()
        users = User.objects.filter(is_superuser=False)
        for user in users:
            for _ in range(options['number']):
                SavedFilters.objects.create(
                    user=user,
                    min_price=fake.random_int(min=1000, max=5000, step=1000),
                    max_price=fake.random_int(min=6000, max=10000, step=1000),
                    min_area=fake.random_int(min=30, max=50, step=5),
                    max_area=fake.random_int(min=70, max=100, step=5),
                    microdistrict=fake.word(),
                    district=fake.city(),
                    house_status=fake.random_element(ResidentialComplex.HouseStatus.values),
                    condition=fake.random_element(Announcement.ConditionType.values),
                    payment_option=fake.random_element(Announcement.PaymentType.values),
                    number_rooms=fake.random_int(min=1, max=20),
                    destination=fake.random_element(Announcement.DestinationType.values),
                )
            print(f'For user ** {user.email} ** created {options["number"]} saved filters')
