# 🎥 YouTube Transcript API Wrapper

Un microservice HTTP (FastAPI + Docker) qui utilise [`youtube-transcript-api`](https://github.com/jdepoix/youtube-transcript-api) pour récupérer les sous-titres des vidéos YouTube **via une simple requête GET**.

## 🚀 Fonctionnalités

- 🔗 Prend une URL YouTube en entrée
- 🧠 Extrait automatiquement le `video_id`
- 📜 Renvoie le transcript en JSON (texte + timecodes)
- 🐳 Déployable via Docker ou Coolify

---

## 📦 Installation locale (avec Docker)

```bash
# Clone ce repo
git clone https://github.com/<ton-user>/youtube-transcriber-api.git
cd youtube-transcriber-api

# Build du conteneur
docker build -t youtube-transcriber .

# Lancer le service sur le port 8080
docker run -p 8080:8080 youtube-transcriber
