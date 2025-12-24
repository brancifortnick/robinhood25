#!/bin/bash
set -e

echo "Running database migrations..."
flask db upgrade

echo "Seeding database (continuing on error if already seeded)..."
flask seed all || echo "Database already seeded, continuing..."

echo "Starting gunicorn..."
exec gunicorn app:app
