#!/bin/bash
set -x

echo Starting celery

exec celery \
--app=scanner \
worker \
--concurrency=2
