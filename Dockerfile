FROM python:3.10-slim

# 🧰 Installation des outils réseau + certificats racines
RUN apt-get update && \
    apt-get install -y \
      curl \
      iputils-ping \
      dnsutils \
      ca-certificates && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

# Variables de version injectées
ENV SOURCE_COMMIT=unknown
ENV IMAGE_TAG=not-set
ENV SCRAPERAPI_KEY=

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"]
