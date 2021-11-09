#!/bin/bash
WAIT_TIME=5

export DRAGONSCALES_PROJECT_PATH=$PWD/tests/projects/test.json
export DRAGONSCALES_REDIS_URL=redis://localhost:6379

virtualenv env > /dev/null
source env/bin/activate > /dev/null
pip install -r requirements.txt > /dev/null

pyflakes dragonscales tests tools || exit 1
black --check dragonscales tests tools wsgi-* || exit 1

pkill redis-server

redis-server > /dev/null &
sleep $WAIT_TIME
redis-cli FLUSHALL 
rq worker queue > /dev/null &

python3 -m pytest $PWD/tests/services/service.py

pkill -xf "${PWD}/env/bin/python ${PWD}/env/bin/rq worker queue"
sleep $WAIT_TIME
pkill redis-server
sleep $WAIT_TIME
