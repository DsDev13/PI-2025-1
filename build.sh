#!/usr/bin/env bash
set -o errexit  # Faz o script falhar se algum comando falhar

pip install -r requirements.txt

export DJANGO_SETTINGS_MODULE=pi2025.settings

python manage.py makemigrations --noinput
python manage.py migrate --noinput
python manage.py collectstatic --noinput
