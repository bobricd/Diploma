import os

from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.management.base import BaseCommand
from faker import Faker
from phonenumber_field.phonenumber import PhoneNumber

from Swipe.users.models import User


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('number', type=int, help='how many owners generate')

    def handle(self, *args, **options):
        file_path = os.path.join(os.getcwd(), 'seed/users', 'profile_image.png')
        with open(file_path, 'rb') as f:
            image_data = f.read()
        profile_image = SimpleUploadedFile(name='profile_image.png', content=image_data, content_type='image/png')
        fake = Faker()
        for _ in range(options['number']):
            user = User.objects.create_user(
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                phone=PhoneNumber.from_string('+38 (073) 242-58-82', region="UA"),
                email=fake.email(),
                password='Swipe12345',
                role=User.RoleName.OWNER,
                profile_image=profile_image,
                agent_first_name="agent",
                agent_last_name="agent",
                agent_phone="+380638881652",
                agent_email="user@example.com",
                switch_to_agent=False,
                is_verified=True
            )
            print('Owner **' + user.email + '** successfully create')
