#!/bin/bash

REDIS_HOST=127.0.0.1
REDIS_PORT=6379
REDIS_POOL=10
REDIS_DB=0

exec twistd -n cyclone_redis_server \
    --redis-host=$REDIS_HOST --redis-port=$REDIS_PORT \
    --redis-pool=$REDIS_POOL --redis-db=$REDIS_DB
