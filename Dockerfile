FROM python:3.10-slim

# 🧰 Installation des certificats racine, utilitaires réseau et d'installation pip
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      ca-certificates \
      curl \
      iputils-ping \
      dnsutils \
    && update-ca-certificates && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Installation des dépendances Python, y compris certifi
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir certifi

# Copie de l'application
COPY app.py .

# Variables de version injectées par Coolify
ENV SOURCE_COMMIT=unknown
ENV IMAGE_TAG=not-set
ENV SCRAPERAPI_KEY=

# Démarrage du serveur
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"]