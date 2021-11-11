#!/bin/bash

export DRAGONSCALES_DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
export DRAGONSCALES_QUEUE_NAME="${DRAGONSCALES_QUEUE_NAME:-default}"
export DRAGONSCALES_QUEUE_URL="${DRAGONSCALES_QUEUE_URL:-redis://localhost:6379}"

rq worker $DRAGONSCALES_QUEUE_NAME
