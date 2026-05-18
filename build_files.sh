#!/bin/bash
set -e

echo "==> Installing dependencies..."
pip install --break-system-packages -r requirements.txt

echo "==> Collecting static files..."
export SECRET_KEY="build-dummy-key-not-used-in-prod"
export DEBUG=False
export ALLOWED_HOSTS=localhost
export USE_S3=False
python manage.py collectstatic --noinput --clear

echo "==> Copying to Vercel output directory..."
mkdir -p staticfiles_build/static
cp -r staticfiles/. staticfiles_build/static/

echo "==> Build complete."
