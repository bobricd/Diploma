import os
import random

import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import AccessToken

from Swipe.announcements.models import Announcement, Image, Application
from Swipe.promotions.models import PromotionType
from Swipe.residential_complexes.models import Advantage, ResidentialComplex, Block, Section, Riser, Floor
from Swipe.settings import BASE_DIR
from Swipe.users.models import User


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture(scope='session')
def django_db_setup(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        User.objects.create_superuser(email='admin@admin.com', password='Swipe12345')
        User.objects.create_user(email='owner@gmail.com', password='Swipe12345', is_verified=True,
                                 role=User.RoleName.OWNER)
        User.objects.create_user(email='builder@gmail.com', password='Swipe12345', is_verified=True,
                                 role=User.RoleName.BUILDER)


@pytest.fixture()
def admin_user(django_user_model):
    return User.objects.get(is_superuser=True)


@pytest.fixture()
def owner_user(django_user_model):
    return User.objects.get(role=User.RoleName.OWNER)


@pytest.fixture()
def builder_user(django_user_model):
    return User.objects.get(role=User.RoleName.BUILDER)


@pytest.fixture()
def authenticated_admin_user(api_client, admin_user):
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {AccessToken.for_user(admin_user)}')
    return api_client


@pytest.fixture()
def authenticated_owner_user(api_client, owner_user):
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {AccessToken.for_user(owner_user)}')
    return api_client


@pytest.fixture()
def authenticated_builder_user(api_client, builder_user):
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {AccessToken.for_user(builder_user)}')
    return api_client


@pytest.fixture
def announcement(owner_user):
    announcement = Announcement.objects.create(
        address="test",
        foundation_document="Own",
        destination="Apartment",
        number_rooms=4,
        layout="Studio",
        condition="Need repair",
        area=55,
        kitchen_area=33,
        has_balcony=True,
        heating_type="Gas",
        payment_option="Cash",
        agent_commission=500,
        communication_method="Messages",
        description="Test",
        price=200000,
        owner=owner_user
    )
    dir_path = os.path.join(BASE_DIR, 'seed/announcements')
    for _ in range(4):
        file_name = random.choice(os.listdir(dir_path))
        with open(os.path.join(dir_path, file_name), 'rb') as f:
            Image.objects.create(image=SimpleUploadedFile(name=file_name, content=f.read()),
                                 announcement=announcement
                                 )
    return announcement


@pytest.fixture
def announcement_moderated(owner_user):
    announcement_moderated = Announcement.objects.create(
        address="test",
        foundation_document="Own",
        destination="Apartment",
        number_rooms=4,
        layout="Studio",
        condition="Need repair",
        area=55,
        kitchen_area=33,
        has_balcony=True,
        heating_type="Gas",
        payment_option="Cash",
        agent_commission=500,
        communication_method="Messages",
        description="Test",
        price=200000,
        owner=owner_user,
        is_moderate=True,
        approved=True
    )
    dir_path = os.path.join(BASE_DIR, 'seed/announcements')
    for _ in range(4):
        file_name = random.choice(os.listdir(dir_path))
        with open(os.path.join(dir_path, file_name), 'rb') as f:
            Image.objects.create(image=SimpleUploadedFile(name=file_name, content=f.read()),
                                 announcement=announcement_moderated
                                 )
    return announcement_moderated


@pytest.fixture
def announcement_moderated_with_rc(announcement_moderated, residential_complex):
    announcement_moderated.residential_complex = residential_complex
    announcement_moderated.save()
    return announcement_moderated


@pytest.fixture()
def promotion_type_obj():
    promotion_type_obj = PromotionType.objects.create(
        name='Test',
        price=50,
        effectivity=75
    )
    return promotion_type_obj


@pytest.fixture()
def advantage():
    logo_path = os.path.join(BASE_DIR, 'seed/residential_complexes/4926341.png')
    with open(logo_path, 'rb') as f:
        logo_data = f.read()
    logo = SimpleUploadedFile(name='logo.png', content=logo_data, content_type='image/png')
    advantage = Advantage.objects.create(
        name='Test',
        logo=logo
    )
    return advantage


@pytest.fixture()
def residential_complex(builder_user):
    residential_complex = ResidentialComplex.objects.create(
        builder=builder_user,
        name="Test",
        description="test RC",
        address="RC",
        contact_first_name="test",
        contact_last_name="test",
        contact_phone="+380734442266",
        contact_email="user@example.com",
        house_status="apartments",
        house_type="multiFamily",
        house_class="economy",
        construction="precastFoundations",
        territory="open",
        communal_payments="payments",
        ceiling_height=10,
        distance_to_sea=400
    )
    return residential_complex


@pytest.fixture()
def block(residential_complex):
    block = Block.objects.create(
        residential_complex=residential_complex,
        name='Block 1'
    )
    return block


@pytest.fixture()
def section(block):
    section = Section.objects.create(
        block=block,
        number=1
    )
    return section


@pytest.fixture()
def riser(section):
    riser = Riser.objects.create(
        section=section,
        number=1
    )
    return riser


@pytest.fixture()
def floor(section):
    floor = Floor.objects.create(
        section=section,
        number=1
    )
    return floor


@pytest.fixture()
def application(announcement_moderated_with_rc):
    application = Application.objects.create(
        residential_complex=announcement_moderated_with_rc.residential_complex,
        announcement=announcement_moderated_with_rc
    )
    return application
