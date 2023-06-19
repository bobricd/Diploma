import os
import random

from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.management.base import BaseCommand
from faker import Faker

from Swipe.residential_complexes.models import Advantage


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('number', type=int, help='how many advantages generate')

    def handle(self, *args, **options):
        fake = Faker()
        dir_path = os.path.join(os.getcwd(), 'seed/residential_complexes/images')
        for _ in range(options['number']):
            file_name = random.choice(os.listdir(dir_path))
            with open(os.path.join(dir_path, file_name), 'rb') as f:
                file_data = f.read()
            advantage = Advantage.objects.create(
                name=fake.word(),
                logo=SimpleUploadedFile(name=file_name, content=file_data)
            )
            print(f'Advantage ** {advantage.name} ** successfully create')
