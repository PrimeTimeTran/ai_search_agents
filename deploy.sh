#!/bin/bash

VERSION=$(git rev-parse --short HEAD)

docker buildx build --platform=linux/amd64 \
  -t us-east1-docker.pkg.dev/ai-search-puzzles/my-repo/ai-search-agents:$VERSION \
  -t us-east1-docker.pkg.dev/ai-search-puzzles/my-repo/ai-search-agents:latest \
  .

docker push us-east1-docker.pkg.dev/ai-search-puzzles/my-repo/ai-search-agents:$VERSION
docker push us-east1-docker.pkg.dev/ai-search-puzzles/my-repo/ai-search-agents:latest

gcloud run deploy ai-search-agents \
  --image us-east1-docker.pkg.dev/ai-search-puzzles/my-repo/ai-search-agents:$VERSION \
  --platform managed \
  --region us-east1 \
  --allow-unauthenticated
