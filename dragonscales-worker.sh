#!/bin/bash

export DRAGONSCALES_QUEUE_NAME="${DRAGONSCALES_QUEUE_NAME:-default}"
export DRAGONSCALES_QUEUE_URL="${DRAGONSCALES_QUEUE_URL:-redis://localhost:6379}"

rq worker --with-scheduler --url $DRAGONSCALES_QUEUE_URL $DRAGONSCALES_QUEUE_NAME $DRAGONSCALES_DELIVERY_QUEUE_NAME
