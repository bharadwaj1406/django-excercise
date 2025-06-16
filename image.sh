#! /bin/bash


##################

# docker image building commands

##################


docker builder prune -a -f

docker build -t django-server:latest .
docker tag django-server:latest bharadwajreddy/django-server:latest

docker login

docker push bharadwajreddy/django-server:latest



