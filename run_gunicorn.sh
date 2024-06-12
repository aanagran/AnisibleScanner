#!/bin/bash
set -x

echo Starting gunicorn

exec gunicorn \
--workers 5 \
--timeout 600 \
--bind=0.0.0.0:8000 \
scanner.wsgi
