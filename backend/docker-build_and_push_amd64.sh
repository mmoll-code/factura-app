#!/bin/bash
# Build and push Docker image for amd64 architecture

IMAGE_NAME="ghcr.io/mmoll-code/fastapi:latest"

echo "Building Docker image for amd64..."
docker buildx build --platform linux/amd64 -t $IMAGE_NAME --push .

echo "Build and push complete." 