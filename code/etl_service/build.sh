#!/bin/sh

# create ssl key pair
openssl req -x509 -nodes -newkey rsa:2048 -keyout ../../deploy/docker/etl_service/key.pem -out ../../deploy/docker/etl_service/cert.pem -sha256 -days 365 \
    -subj "/CN=localhost"

#build docker image
docker build . -t etl_service