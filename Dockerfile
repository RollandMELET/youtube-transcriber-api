FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

# Variables de version injectées par Coolify
ENV SOURCE_COMMIT=unknown
ENV IMAGE_TAG=not-set
ENV SCRAPERAPI_KEY=

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"]

# Force DNS Google public
ENV DNS_SERVER=8.8.8.8