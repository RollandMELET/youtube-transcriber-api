from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse, parse_qs
import os
import requests

app = FastAPI()

# variables d’environnement
SCRAPERAPI_KEY = os.getenv("SCRAPERAPI_KEY", "")
GIT_COMMIT      = os.getenv("SOURCE_COMMIT", "unknown")
IMAGE_TAG       = os.getenv("IMAGE_TAG", "not-set")

# URL de l’API ScraperAPI pour le quota
SCRAPER_QUOTA_URL = "https://api.scraperapi.com/quota"

def extract_video_id(url: str):
    parsed = urlparse(url)
    if parsed.hostname == "youtu.be":
        return parsed.path[1:]
    if parsed.hostname in ("www.youtube.com", "youtube.com"):
        return parse_qs(parsed.query).get("v", [None])[0]
    return None

def get_scraper_quota():
    """Interroge l’API ScraperAPI pour récupérer l’état du quota."""
    if not SCRAPERAPI_KEY:
        return None
    try:
        r = requests.get(
            SCRAPER_QUOTA_URL,
            params={"api_key": SCRAPERAPI_KEY},
            timeout=5
        )
        return r.json()  # { success, used, remaining, monthly_limit, reset_at, ... }
    except Exception:
        return None

@app.get("/quota")
def quota():
    info = get_scraper_quota()
    if not info:
        return JSONResponse(
            status_code=500,
            content={"error": "Impossible de récupérer le quota ScraperAPI"}
        )
    return info

@app.get("/transcript")
def get_transcript(url: str = Query(..., description="URL YouTube à transcrire")):
    video_id = extract_video_id(url)
    if not video_id:
        return JSONResponse(400, {"error": "URL YouTube invalide"})

    if not SCRAPERAPI_KEY:
        return JSONResponse(500, {"error": "La variable SCRAPERAPI_KEY n’est pas configurée"})

    proxy = f"http://scraperapi:{SCRAPERAPI_KEY}@proxy-server.scraperapi.com:8001"
    proxies = {"http": proxy, "https": proxy}

    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id, proxies=proxies)
        return transcript

    except Exception as e:
        msg = str(e).lower()
        # quota dépassé ou IP bloquée
        if any(k in msg for k in ("quota", "403", "blocked")):
            quota_info = get_scraper_quota()
            payload = {"error": "ScraperAPI quota exceeded or IP blocked"}
            if quota_info:
                # n’ajoute que les champs qui t’intéressent
                payload["quota_remaining"] = quota_info.get("remaining")
                payload["quota_limit"]     = quota_info.get("monthly_limit")
                payload["quota_resets_at"] = quota_info.get("reset_at")
            return JSONResponse(status_code=429, content=payload)

        # autre erreur (ex: vidéo sans transcript)
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.get("/version")
def version():
    return {
        "service": "youtube-transcriber-api",
        "commit": GIT_COMMIT,
        "image": IMAGE_TAG
    }
