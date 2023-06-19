import random

from django.core.management.base import BaseCommand

from Swipe.announcements.models import Announcement, Application


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('number', type=int, help='how many applications generate')

    def handle(self, *args, **options):
        announcements = Announcement.objects.filter(is_moderate=True, applications__isnull=True)
        if announcements:
            for announcement in announcements:
                Application.objects.create(
                    residential_complex=announcement.residential_complex,
                    announcement=announcement
                )
                print(f'Application for announcement ** {announcement.id} ** successfully created')
