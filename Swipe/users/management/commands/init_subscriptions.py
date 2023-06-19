import random

from dateutil.relativedelta import relativedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
from faker import Faker

from Swipe.users.models import User, Subscription, SubscriptionType


class Command(BaseCommand):
    def handle(self, *args, **options):
        fake = Faker()
        subscription_types = SubscriptionType.objects.all()
        users = User.objects.filter(role=User.RoleName.OWNER)
        for user in users:
            subscription_type = random.choice(subscription_types)
            Subscription.objects.create(
                auto_renewal=fake.boolean(chance_of_getting_true=75),
                subscription_type=subscription_type,
                owner=user,
                date=timezone.now().date() + relativedelta(months=1)
            )
            print(f'Owner **{user.email}** with subscription * {subscription_type} *')