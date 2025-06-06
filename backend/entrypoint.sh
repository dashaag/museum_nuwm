#!/bin/sh

# Exit immediately if a command exits with a non-zero status.
set -e

# Wait for DB to be ready
# This is a simple wait, a more robust solution might use nc or pg_isready in a loop
# Docker-compose's depends_on with healthcheck is the primary mechanism for this.
echo "Entrypoint: Waiting for database to be ready..."

# Apply database migrations using Alembic
echo "Entrypoint: Applying Alembic database migrations..."
alembic upgrade head

# Check if INIT_DB is true and run initial data seeding
# The initial_data.py script should be idempotent or check if data already exists.
if [ "${INIT_DB}" = "true" ] ; then
  echo "Entrypoint: INIT_DB is true. Running initial data seeding..."
  python initial_data.py
else
  echo "Entrypoint: INIT_DB is not 'true'. Skipping initial data seeding."
fi

# Start Uvicorn server
# --reload is useful for development. For production, you might remove it or use a process manager like Gunicorn.
echo "Entrypoint: Starting Uvicorn server..."
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
