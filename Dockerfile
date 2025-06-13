FROM python:3.10-slim

# 1️⃣ Ajout des certificats racine + outils réseau
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      ca-certificates \
      curl \
      iputils-ping \
      dnsutils && \
    update-ca-certificates && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

# Variables de version injectées par Coolify
ENV SOURCE_COMMIT=unknown
ENV IMAGE_TAG=not-set
ENV SCRAPERAPI_KEY=

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"]
