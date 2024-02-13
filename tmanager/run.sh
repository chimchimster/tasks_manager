#!/bin/bash

env_path=.env

dotenv () {
  set -a
  [ -f $env_path ] && source $env_path
  set +a
}

dotenv
celery -A tmanager worker --loglevel=info && gunicorn --workers=7 tmanager.wsgi --access-logfile '-' --bind 0.0.0.0:8000
