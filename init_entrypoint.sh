#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
  echo "Waiting for postgres..."

  while ! nc -z $SQL_HOST $SQL_PORT; do
    sleep 0.1
  done

  echo "PostgreSQL started"
fi
  python3 manage.py migrate
  python3 manage.py init_admin
  python3 manage.py collectstatic --no-input
  python3 manage.py create_builders 10
  python3 manage.py create_owners 10
  python3 manage.py create_subscription_types 5
  python3 manage.py init_subscriptions
  python3 manage.py create_messages
  python3 manage.py add_saved_filters 2
  python3 manage.py create_notaries 15
  python3 manage.py create_promotion_types 5
  python3 manage.py create_advantages 10
  python3 manage.py create_residential_complex
  python3 manage.py create_announcements 20
  python3 manage.py create_announcements_moderated 10
  python3 manage.py create_applications 10
  python3 manage.py create_announcements_moderated 10
  python3 manage.py allow_applications 50
exec "$@"