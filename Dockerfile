FROM python:3.10-slim

# 🧰 Installation des outils réseau de diagnostic
RUN apt-get update && \
    apt-get install -y curl iputils-ping dnsutils && \
    rm -rf /var/lib/apt/lists/*

# 📁 Création du répertoire de travail
WORKDIR /app

# 📦 Installation des dépendances Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 🐍 Code source
COPY app.py .

# 🌐 Variables d'environnement injectées par Coolify
ENV SOURCE_COMMIT=unknown
ENV IMAGE_TAG=not-set
ENV SCRAPERAPI_KEY=

# 🚀 Lancement de l'application
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"]
