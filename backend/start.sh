#!/bin/sh

# check migrations
python3 manage.py migrate

# check and creause superuser, if it dosn't exist yet
python3 manage.py shell -c "
from django.contrib.auth import get_user_model;
User = get_user_model();
if not User.objects.filter(is_superuser=True).exists():
    print('Creating superuser...');
    User.objects.create_superuser('admin', 'admin@example.com', 'admin');
else:
    print('Superuser already exists.');
"
