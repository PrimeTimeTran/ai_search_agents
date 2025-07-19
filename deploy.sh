#!/bin/bash

VERSION=$(git rev-parse --short HEAD)

docker buildx build --platform=linux/amd64 \
  -t us-east1-docker.pkg.dev/ai-search-puzzles/my-repo/ai-search-agent:$VERSION \
  -t us-east1-docker.pkg.dev/ai-search-puzzles/my-repo/ai-search-agent:latest \
  .

docker push us-east1-docker.pkg.dev/ai-search-puzzles/my-repo/ai-search-agent:$VERSION
docker push us-east1-docker.pkg.dev/ai-search-puzzles/my-repo/ai-search-agent:latest

gcloud run deploy ai-search-agent \
  --image us-east1-docker.pkg.dev/ai-search-puzzles/my-repo/ai-search-agent:$VERSION \
  --platform managed \
  --region us-east1 \
  --allow-unauthenticated
