from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse, parse_qs
import os
import certifi

# ⚠️ Forcer l'utilisation du bundle de certificats de certifi
os.environ['SSL_CERT_FILE'] = certifi.where()

app = FastAPI()

# Lecture des variables d’environnement
iSCRAPERAPI_KEY = os.getenv("SCRAPERAPI_KEY", "")
GIT_COMMIT = os.getenv("SOURCE_COMMIT", "unknown")
IMAGE_TAG = os.getenv("IMAGE_TAG", "not-set")

 def extract_video_id(url: str):
    parsed_url = urlparse(url)
    if parsed_url.hostname == "youtu.be":
        return parsed_url.path[1:]
    elif parsed_url.hostname in ["www.youtube.com", "youtube.com"]:
        return parse_qs(parsed_url.query).get("v", [None])[0]
    return None

@app.get("/transcript")
def get_transcript(url: str):
    video_id = extract_video_id(url)
    if not video_id:
        return JSONResponse(status_code=400, content={"error": "Invalid YouTube URL"})

    if not SCRAPERAPI_KEY:
        return JSONResponse(status_code=500, content={"error": "SCRAPERAPI_KEY is not configured"})

    # Utilisation du bon host proxy\    proxy_auth = f"http://scraperapi:{SCRAPERAPI_KEY}@proxy-server.scraperapi.com:8001"
    proxies = {
        "http": proxy_auth,
        "https": proxy_auth
    }

    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id, proxies=proxies)
        return transcript
    except Exception as e:
        msg = str(e)
        if any(keyword in msg.lower() for keyword in ("quota", "403", "blocked")):
            return JSONResponse(status_code=429, content={"error": "ScraperAPI quota exceeded or IP blocked"})
        return JSONResponse(status_code=500, content={"error": msg})

@app.get("/version")
def version():
    return {
        "service": "youtube-transcriber-api",
        "commit": GIT_COMMIT,
        "image": IMAGE_TAG
    }