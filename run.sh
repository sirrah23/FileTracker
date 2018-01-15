#!/bin/bash

# Run the celery worker for async tasks
pipenv run celery -A dbxcelery.tasks worker -B --loglevel=info &
# Run the Django web application
pipenv run python filetracker/manage.py runserver &
