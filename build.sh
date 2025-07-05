#!/usr/bin/env bash
set -o errexit

pip install --upgrade pip
pip install -r requirements.txt

cd src
mkdir -p staticfiles
python manage.py collectstatic --no-input

python manage.py migrate

cd ..