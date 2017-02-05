#!/bin/sh
cd /home/pi/Documents/projects/django-alpr/testalpr/live_alpr-master
python -u /home/pi/Documents/projects/django-alpr/testalpr/live_alpr/live_alpr.py | tee log
