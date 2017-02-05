#!/bin/bash

# Name of the application
NAME="LicensesPlates"
# Django project directory
DJANGODIR=/home/pi/Documents/projects/django-alpr
# we will communicate using this unix socket
SOCKFILE=/home/pi/Documents/projects/django-alpr/run/gunicorn.sock
# the user to run as
USER=pi
# the group to run as
GROUP=
# how many worker processes should Gunicorn spawn
NUM_WORKERS=3
# which settings file should Django use
DJANGO_SETTINGS_MODULE=LicensesPlates.settings
# WSGI module name
DJANGO_WSGI_MODULE=LicensesPlates.wsgi

echo "Starting $NAME as `whoami`"

# Activate the virtual environment
cd $DJANGODIR
source /home/pi/venv/venv1/bin/activate
export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
export PYTHONPATH=$DJANGODIR:$PYTHONPATH

# Create the run directory if it doesn't exist
RUNDIR=$(dirname $SOCKFILE)
test -d $RUNDIR || mkdir -p $RUNDIR

# Start your Django Unicorn
# Programs meant to be run under supervisor should not daemonize themselves (do not use --daemon)
exec ../bin/gunicorn ${DJANGO_WSGI_MODULE}:application \
  --name $NAME \
  --workers $NUM_WORKERS \
  --user=$USER --group=$GROUP \
  --bind=unix:$SOCKFILE \
  --log-level=debug \
  --log-file=-