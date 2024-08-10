#!/usr/bin/env bash

cd "$(dirname, "$0")"

docker build -t fineness-prediction-service:testv1 ..

docker run -d --rm -p 9696:9696 fineness-prediction-service:testv1

pipenv run python integration_test.py