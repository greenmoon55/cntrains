#!/bin/bash
python /src/manage.py runserver 0.0.0.0:80 --insecure > /var/log/django.log 2>&1
