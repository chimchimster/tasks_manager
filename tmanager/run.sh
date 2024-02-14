#!/bin/bash


cd tmanager && celery -A tmanager beat --loglevel=info & cd tmanager && celery -A tmanager worker --loglevel=info & cd tmanager && gunicorn --workers=7 tmanager.wsgi --access-logfile '-' --bind 0.0.0.0:8000
