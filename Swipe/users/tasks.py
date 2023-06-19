from celery import shared_task
from dateutil.relativedelta import relativedelta
from django.utils import timezone

from Swipe.users.models import Subscription


@shared_task
def renew_subscriptions_task():
    today = timezone.now().date()
    subscriptions = Subscription.objects.\
        filter(date__lte=today, auto_renewal=True).\
        update(date=today + relativedelta(months=1))
    # subscriptions.filter(auto_renewal=True).update(date=today + relativedelta(months=1))
    # subscriptions.filter(auto_renewal=False).delete()
    print(subscriptions)
    print("Subscriptions are successfully auto renewal")
