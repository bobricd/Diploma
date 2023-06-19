from django.core.management import BaseCommand

from Swipe.announcements.models import Announcement


class Command(BaseCommand):

    def handle(self, *args, **options):
        Announcement.objects.all().delete()
        print(f'Announcements deleted successfully')
