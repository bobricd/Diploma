import os
import random

from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.management.base import BaseCommand
from faker import Faker
from geopy import Nominatim

from Swipe.announcements.models import Announcement, Image
from Swipe.promotions.models import PromotionType
from Swipe.residential_complexes.models import ResidentialComplex
from Swipe.users.models import User


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('number', type=int, help='how many announcements generate')

    def handle(self, *args, **options):
        images_dir_path = os.path.join(os.getcwd(), 'seed/announcements')
        fake = Faker()
        users = User.objects.filter(is_superuser=False, role=User.RoleName.OWNER)
        residential_complexes = ResidentialComplex.objects.all()
        promotion_types = PromotionType.objects.all()
        geolocator = Nominatim(user_agent="Swipe")
        for _ in range(options['number']):
            address = geolocator.reverse(fake.local_latlng()[:2])
            while address is None:
                address = geolocator.reverse(fake.local_latlng()[:2])

            announcement = Announcement.objects.create(
                address=address,
                owner=random.choice(users),
                residential_complex=random.choice(residential_complexes),
                foundation_document=fake.random_element(Announcement.FoundationDocumentType.values),
                destination=fake.random_element(Announcement.DestinationType.values),
                number_rooms=fake.random_int(min=1, max=30),
                layout=fake.random_element(Announcement.LayoutType.values),
                condition=fake.random_element(Announcement.ConditionType.values),
                area=fake.random_int(min=50, max=500),
                kitchen_area=fake.random_int(min=5, max=50),
                has_balcony=fake.boolean(chance_of_getting_true=75),
                heating_type=fake.random_element(Announcement.HeatingType.values),
                payment_option=fake.random_element(Announcement.PaymentType.values),
                agent_commission=fake.random_element(Announcement.AgentCommission.values),
                communication_method=fake.random_element(Announcement.CommunicationMethod.values),
                description=fake.text(max_nb_chars=200),
                price=fake.random_int(min=1000, max=100000),
                promotion_type=random.choice(promotion_types)
            )
            for index in range(random.randrange(1, 5)):
                image_name = random.choice(os.listdir(images_dir_path))
                with open(os.path.join(images_dir_path, image_name), 'rb') as f:
                    image_data = f.read()
                Image.objects.create(
                    announcement=announcement,
                    image=SimpleUploadedFile(name=image_name, content=image_data),
                )

        print(f'Announcements created successfully')
