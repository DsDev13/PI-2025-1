#!/usr/bin/env bash

pip install -r requirements.txt

# Garante que o ambiente do Django seja usado corretamente
export DJANGO_SETTINGS_MODULE=pi2025.settings

python manage.py makemigrations apconect
python manage.py migrate
python manage.py collectstatic --noinput
