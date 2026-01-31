#!/usr/bin/env bash
set -e

echo " Running Celery worker pre-start checks..."
python /app/app/celeryworker_pre_start.py

echo " Starting Celery worker..."
exec celery worker \
    -A app.worker \
    -l info \
    -Q main-queue \
    -c 1
