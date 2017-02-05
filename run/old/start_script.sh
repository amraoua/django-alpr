#!/bin/bash
WORKING_DIR= /home/pi/Documents/projects/django-alpr
ACTIVATE_PATH= /home/pi/venv/venv1/bin/activate
cd ${WORKING_DIR}
source ${ACTIVATE_PATH}
exec $@