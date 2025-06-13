from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse, parse_qs

app = FastAPI()

def extract_video_id(url: str):
    """Extrait le video ID depuis l'URL YouTube"""
    parsed_url = urlparse(url)
    if parsed_url.hostname in ["youtu.be"]:
        return parsed_url.path[1:]
    elif parsed_url.hostname in ["www.youtube.com", "youtube.com"]:
        return parse_qs(parsed_url.query).get("v", [None])[0]
    return None

@app.get("/transcript")
def get_transcript(url: str = Query(..., description="URL de la vidéo YouTube")):
    video_id = extract_video_id(url)
    if not video_id:
        return JSONResponse(status_code=400, content={"error": "Invalid YouTube URL"})

    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        return transcript
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
