import random

from django.core.management.base import BaseCommand

from Swipe.announcements.models import Application


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('percent', type=int, help='how many applications allow in percents')

    def handle(self, *args, **options):
        applications = Application.objects.all()
        percent_allow = options['percent']
        if percent_allow > 100:
            percent_allow = 100

        if applications:
            for _ in range(int(len(applications)*(percent_allow/100))):
                application = random.choice(applications)
                applications = applications.exclude(id=application.id)
                announcement = application.announcement
                residential_complex = application.residential_complex
                blocks = random.choice(residential_complex.blocks.all())
                section = random.choice(blocks.sections.all())
                announcement.floor = random.choice(section.floors.all())
                announcement.riser = random.choice(section.risers.all())
                print(f'Announcement ** {announcement.id} ** successfully add to residential complex'
                      f' **{residential_complex.name}**')
        print(f'applications not found')
