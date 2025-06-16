#! /bin/bash


##################

# docker image building commands

##################


docker builder prune -a -f

docker compose up --build -d



