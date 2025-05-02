from fastapi import FastAPI
from backend.services.audio import audio_router
from backend.services.stt import stt_router
from backend.services.summary import summary_router

app = FastAPI(
    title="AI 기반 유튜브 영상 요약 서비스",
    description="유튜브 영상 링크를 입력하면 자동으로 요약된 텍스트를 제공",
    version="1.25.1"
)

app.include_router(audio_router)
app.include_router(stt_router)
app.include_router(summary_router)