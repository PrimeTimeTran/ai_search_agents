FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ARG COMMIT_SHA
ARG COMMIT_URL
ARG WORKFLOW_RUN_URL

ENV COMMIT_SHA=${COMMIT_SHA}
ENV COMMIT_URL=${COMMIT_URL}
ENV WORKFLOW_RUN_URL=${WORKFLOW_RUN_URL}

EXPOSE 8080

CMD ["python", "app.py"]
