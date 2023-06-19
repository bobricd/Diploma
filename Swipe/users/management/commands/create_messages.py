import os
import random

from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.management.base import BaseCommand
from faker import Faker

from Swipe.users.models import User, Message


class Command(BaseCommand):

    def handle(self, *args, **options):
        dir_path = os.path.join(os.getcwd(), 'seed/messages')
        file_name = random.choice(os.listdir(dir_path))
        with open(os.path.join(dir_path, file_name), 'rb') as f:
            file_data = f.read()
        file = SimpleUploadedFile(name=file_name, content=file_data)
        fake = Faker()
        admin = User.objects.get(is_superuser=True)
        file_choices = [file, None]
        owners = User.objects.filter(role=User.RoleName.OWNER)
        for owner in owners:
            for _ in range(random.randrange(1, 4)):
                Message.objects.create(
                    sender=owner,
                    text=fake.sentence(nb_words=10),
                    receiver=admin,
                    file=random.choice(file_choices)
                )
            Message.objects.create(
                sender=admin,
                text=fake.sentence(nb_words=10),
                receiver=owner,
                file=random.choice(file_choices)
            )
            print('Messages for **' + owner.email + '** successfully created')
