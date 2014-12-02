#!/usr/bin/env bash
#
# To be executed from project root dir.
#
# Usage: $0 [port]
#   port: listening port; defaults to 8000
PORT=${1:-8000}
. ~/virtualenvs/sla-dashboard/bin/activate
./manage.py runserver 0.0.0.0:$PORT
