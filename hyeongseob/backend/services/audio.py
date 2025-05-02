from fastapi import APIRouter
from backend.utils import download_audio
from pydantic import BaseModel

audio_router = APIRouter(prefix="/audio", tags=["Audio"])

class UrlData(BaseModel):
    url: str

@audio_router.post("/extraction")
def extraction_audio(data: UrlData):
    data = data.model_dump()
    audio_path = download_audio(data["url"])

    try:
        return audio_path
    except Exception as e:
        print("오류 발생:", e)