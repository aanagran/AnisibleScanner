#!/bin/bash
set -x

echo Starting celery

exec celery \
--app=scanner \
beat
