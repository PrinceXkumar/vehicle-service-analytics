#!/bin/bash

echo "Starting Build..."
python3 -m pip install -r requirements.txt

echo "Running Migrations..."
python3 manage.py migrate --noinput

echo "Collecting Static Files..."
python3 manage.py collectstatic --noinput --clear

echo "Build Finished!"
