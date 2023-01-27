#!/bin/sh

# create ssl key pair
openssl req -x509 -nodes -newkey rsa:2048 -keyout ./graph-connector/key.pem -out ./graph-connector/cert.pem -sha256 -days 365 \
    -subj "/CN=localhost"

#build docker images
cd ../../code/graph-connector || exit
docker build . -t graph-connector

cd ../disco-graph/ui
docker build . -t disco-graph-ui