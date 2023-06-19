from django.core.management.base import BaseCommand

from Swipe.users.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):

        if User.objects.count() == 0:
            email = 'admin@admin.com'
            password = 'Swipe12345'
            print(f'Creating account for {email}')
            User.objects.create_superuser(email=email, password=password)
        else:
            print('Admin already initialize')
