#!/bin/bash

export DRAGONSCALES_DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
export DRAGONSCALES_LOGGER_LEVEL="${DRAGONSCALES_LOGGER_LEVEL:-INFO}"
export DRAGONSCALES_LOGGER_PATH="${DRAGONSCALES_LOGGER_PATH:-dragonscales.log}"
export DRAGONSCALES_LOGGER_MAX_BYTES="${DRAGONSCALES_LOGGER_MAX_BYTES:-1048576}"
export DRAGONSCALES_PROJECT_PATH="${DRAGONSCALES_PROJECT_PATH:-project.json}"
export DRAGONSCALES_SERVICE_ADDRESS="${DRAGONSCALES_SERVICE_ADDRESS:-0.0.0.0:5003}"
export DRAGONSCALES_QUEUE_URL="${DRAGONSCALES_QUEUE_URL:-redis://localhost:6379}"

if ! [ -f "$DRAGONSCALES_PROJECT_PATH" ]; then
    echo "${DRAGONSCALES_PROJECT_PATH} does not exist."
    exit -1
fi

gunicorn --chdir $DRAGONSCALES_DIR --bind $DRAGONSCALES_SERVICE_ADDRESS --worker-class=uvicorn.workers.UvicornWorker wsgi-dragonscales:app
