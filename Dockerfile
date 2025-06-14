FROM python:3.10-slim

# installation certs & outils réseau
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      ca-certificates \
      curl \
      iputils-ping \
      dnsutils && \
    update-ca-certificates && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# dépendances
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir certifi

# Variables SSL pour Python & Requests
ENV SSL_CERT_FILE=/usr/local/lib/python3.10/site-packages/certifi/cacert.pem
ENV REQUESTS_CA_BUNDLE=/usr/local/lib/python3.10/site-packages/certifi/cacert.pem
ENV PYTHONHTTPSVERIFY=0

COPY app.py .

# versioning et clé
ENV SOURCE_COMMIT=unknown
ENV IMAGE_TAG=not-set
ENV SCRAPERAPI_KEY=

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"]
