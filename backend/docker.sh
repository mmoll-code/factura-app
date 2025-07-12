#!/bin/bash

case "$1" in
  up)
    docker-compose up --build
    ;;
  down)
    docker-compose down
    ;;
  build)
    docker-compose build
    ;;
  restart|rebuild)
    docker-compose down
    docker-compose build
    docker-compose up -d
    ;;
  *)
    echo "Usage: $0 {up|down|build|restart}"
    exit 1
esac 