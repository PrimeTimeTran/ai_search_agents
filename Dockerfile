FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8080
ARG COMMIT_SHA
ARG COMMIT_URL

ENV COMMIT_SHA=$COMMIT_SHA
ENV COMMIT_URL=$COMMIT_URL
CMD ["python", "app.py"]

