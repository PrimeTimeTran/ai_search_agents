Enable GCP CLI services

```sh
gcloud services enable run.googleapis.com
gcloud services enable artifactregistry.googleapis.com
```

Project initialization

```sh
gcloud config set project ai-search-puzzles
gcloud config set run/region us-east1
```

Building image

```sh
# MacOS Only
docker buildx build --platform=linux/amd64 -t us-east1-docker.pkg.dev/ai-search-puzzles/my-repo/flask-app .
# Other Platforms
# docker build -t us-east1-docker.pkg.dev/ai-search-puzzles/my-repo/flask-app .
```

Create Artifact Registry Repo

```sh
gcloud artifacts repositories create my-repo \
  --repository-format=docker \
  --location=us-east1
```

Push Image to Artifact Registry

```sh
docker push us-east1-docker.pkg.dev/ai-search-puzzles/my-repo/flask-app
```

Deploy to Cloud Run

```sh
gcloud run deploy flask-app \
  --image us-east1-docker.pkg.dev/ai-search-puzzles/my-repo/flask-app \
  --platform managed \
  --allow-unauthenticated \
  --region us-east1
```
