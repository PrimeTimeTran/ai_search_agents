#!/bin/bash

VERSION=$(git rev-parse --short HEAD)  # or use date

docker buildx build --platform=linux/amd64 \
  -t us-east1-docker.pkg.dev/ai-search-puzzles/my-repo/flask-app:$VERSION \
  -t us-east1-docker.pkg.dev/ai-search-puzzles/my-repo/flask-app:latest \
  .

docker push us-east1-docker.pkg.dev/ai-search-puzzles/my-repo/flask-app:$VERSION
docker push us-east1-docker.pkg.dev/ai-search-puzzles/my-repo/flask-app:latest

gcloud run deploy flask-app \
  --image us-east1-docker.pkg.dev/ai-search-puzzles/my-repo/flask-app:$VERSION \
  --platform managed \
  --region us-east1 \
  --allow-unauthenticated
