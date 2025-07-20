#!/bin/bash

set -e

VERSION=$(git rev-parse --short HEAD)
COMMIT_URL="https://github.com/$GIT_REPO/commit/$GIT_COMMIT_SHA"

echo "🔨 Building image for commit: $VERSION"
echo "🔗 Commit URL: $COMMIT_URL"

docker buildx build --platform=linux/amd64 \
  --push \
  --build-arg COMMIT_SHA=$VERSION \
  --build-arg COMMIT_URL=$COMMIT_URL \
  --build-arg WORKFLOW_RUN_URL=$WORKFLOW_RUN_URL \
  -t us-east1-docker.pkg.dev/ai-search-puzzles/my-repo/ai-search-agents:$VERSION \
  -t us-east1-docker.pkg.dev/ai-search-puzzles/my-repo/ai-search-agents:latest \
  .

echo "🚀 Deploying to Cloud Run..."

gcloud run deploy ai-search-agents \
  --image us-east1-docker.pkg.dev/ai-search-puzzles/my-repo/ai-search-agents:$VERSION \
  --platform managed \
  --region us-east1 \
  --allow-unauthenticated

echo "✅ Deployment complete: $COMMIT_URL"
echo "::notice title=Deployment complete::View commit $COMMIT_URL"
echo "::notice title=Commit::https://github.com/$GIT_REPO/commit/$GIT_COMMIT_SHA"
echo "::notice title=Workflow Run::${WORKFLOW_RUN_URL}"
