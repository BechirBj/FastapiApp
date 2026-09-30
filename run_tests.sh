#!/bin/bash

set -e

CONTAINER_NAME="fastapi-users"
IMAGE_NAME="fastapi-users"
PYTHON="./venv/bin/python"

echo "======================================"
echo "1. Running unit and integration tests"
echo "======================================"

$PYTHON -m pytest tests/unit tests/integration

echo "======================================"
echo "2. Building Docker image"
echo "======================================"

docker build -t $IMAGE_NAME .

echo "======================================"
echo "3. Starting FastAPI container"
echo "======================================"

docker rm -f $CONTAINER_NAME 2>/dev/null || true

docker run -d \
    --name $CONTAINER_NAME \
    -p 8000:8000 \
    $IMAGE_NAME

echo "======================================"
echo "4. Waiting for FastAPI"
echo "======================================"

sleep 3

echo "======================================"
echo "5. Running E2E tests"
echo "======================================"

$PYTHON -m pytest tests/e2e

echo "======================================"
echo "6. Cleaning up"
echo "======================================"

docker stop $CONTAINER_NAME
docker rm $CONTAINER_NAME

echo "======================================"
echo "ALL TESTS PASSED"
echo "======================================"