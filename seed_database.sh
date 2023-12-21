#!/bin/bash

rm db.sqlite3
rm -rf ./venueapi/migrations
python3 manage.py migrate
python3 manage.py makemigrations venueapi
python3 manage.py migrate venueapi
python3 manage.py loaddata users
python3 manage.py loaddata tokens
python3 manage.py loaddata bands
python3 manage.py loaddata venues
python3 manage.py loaddata concerts
python3 manage.py loaddata openers
python3 manage.py loaddata favorites