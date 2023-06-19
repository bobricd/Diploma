import os
import random

from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.management.base import BaseCommand
from faker import Faker

from Swipe.residential_complexes.models import ResidentialComplex, Block, Section, Floor, Riser, News, Document, Image, \
    Advantage
from Swipe.users.models import User


class Command(BaseCommand):
    # def add_arguments(self, parser):
    #     parser.add_argument('number', type=int, help='how many residential complex generate')

    def handle(self, *args, **options):
        documents_dir_path = os.path.join(os.getcwd(), 'seed/residential_complexes/documents')
        images_dir_path = os.path.join(os.getcwd(), 'seed/residential_complexes/images')
        fake = Faker()
        builders = User.objects.filter(role=User.RoleName.BUILDER)
        advantages = Advantage.objects.all()
        for builder in builders:
            residential_complex = ResidentialComplex.objects.create(
                builder=builder,
                name=fake.company(),
                description=fake.text(),
                address=fake.address(),
                contact_first_name=fake.first_name(),
                contact_last_name=fake.last_name(),
                contact_phone=fake.phone_number(),
                contact_email=fake.email(),
                house_status=fake.random_element(ResidentialComplex.HouseStatus.values),
                house_type=fake.random_element(ResidentialComplex.HouseType.values),
                house_class=fake.random_element(ResidentialComplex.HouseClass.values),
                construction=fake.random_element(ResidentialComplex.ConstructionType.values),
                territory=fake.random_element(ResidentialComplex.TerritoryType.values),
                distance_to_sea=fake.random_int(min=1, max=100),
                communal_payments=fake.random_element(ResidentialComplex.CommunalPayment.values),
                ceiling_height=fake.random_int(min=250, max=400) / 100.0,
                gas=fake.random_element(ResidentialComplex.UtilitiesType.values),
                heating=fake.random_element(ResidentialComplex.UtilitiesType.values),
                sewerage=fake.random_element(ResidentialComplex.UtilitiesType.values),
                water_supply=fake.random_element(ResidentialComplex.UtilitiesType.values),
            )
            for block_index in range(random.randrange(1, 5)):
                block = Block.objects.create(
                    residential_complex=residential_complex,
                    name=f'Block {block_index + 1}'
                )
                for section_index in range(random.randrange(1, 3)):
                    section = Section.objects.create(
                        block=block,
                        number=section_index + 1
                    )
                    for floor_index in range(random.randrange(1, 3)):
                        Floor.objects.create(
                            section=section,
                            number=floor_index + 1
                        )
                    for riser_index in range(random.randrange(1, 3)):
                        Riser.objects.create(
                            section=section,
                            number=riser_index + 1
                        )
            for _ in range(random.randrange(1, 5)):
                News.objects.create(
                    residential_complex=residential_complex,
                    title=fake.sentence(nb_words=5),
                    text=fake.paragraph(nb_sentences=3),
                )
            for _ in range(random.randrange(1, 5)):
                document_name = random.choice(os.listdir(documents_dir_path))
                with open(os.path.join(documents_dir_path, document_name), 'rb') as f:
                    document_data = f.read()
                Document.objects.create(
                    residential_complex=residential_complex,
                    is_excel=False,
                    file=SimpleUploadedFile(name=document_name, content=document_data)
                )
            for index in range(random.randrange(1, 5)):
                image_name = random.choice(os.listdir(images_dir_path))
                with open(os.path.join(images_dir_path, image_name), 'rb') as f:
                    image_data = f.read()
                Image.objects.create(
                    residential_complex=residential_complex,
                    image=SimpleUploadedFile(name=image_name, content=image_data),
                    order=index + 1
                )
            for _ in range(random.randrange(1, 5)):
                residential_complex.advantages.add(random.choice(advantages))

            print(f'Residential complex ** {residential_complex.name} ** created successfully')
