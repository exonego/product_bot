#!/bin/bash
set -e

echo "Applying alembic migrations..."
alembic upgrade head
echo "Alembic migrations applied succesfully."
echo "Starting app..."
exec python main.py
