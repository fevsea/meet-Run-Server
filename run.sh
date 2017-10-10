#!/usr/bin/env bash
killall python
source ~/meetNRun/restEnv/bin/activate
nohup python manage.py runserver 0.0.0.0:8000&
