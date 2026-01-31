#!/usr/bin/env bash
set -e

echo " Starting backend pre-start tasks..."

# Wait for DB / pre-checks
echo "Running backend pre-start checks..."
python /app/app/backend_pre_start.py

# Run migrations
echo " Running database migrations..."
alembic upgrade head

# Create initial data
echo " Creating initial data..."
python /app/app/initial_data.py

echo " Pre-start tasks completed successfully"
