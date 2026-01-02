#!/bin/bash
# Wrapper script to run docker-compose from root directory

cd "$(dirname "$0")"
docker-compose -f docker/docker-compose.yml "$@"
