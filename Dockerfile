FROM python:3.11-slim
WORKDIR /app
ENV COMMIT_SHA=unknown
ENV COMMIT_URL=unknown

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8080
CMD ["python", "app.py"]
