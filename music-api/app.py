from fastapi import FastAPI

from database import init_database

from routes.search import router as search_router
from routes.stream import router as stream_router
from routes.play import router as play_router
from routes.download import router as download_router
from routes.song import router as song_router
from routes.health import router as health_router


app = FastAPI(
    title="WLZBI Music API",
    description="Professional Music Streaming API by WLZBI",
    version="1.0.0"
)


@app.on_event("startup")
async def startup():
    await init_database()


# Register Routers
app.include_router(search_router)
app.include_router(stream_router)
app.include_router(play_router)
app.include_router(download_router)
app.include_router(song_router)
app.include_router(health_router)


@app.get("/", tags=["Home"])
async def home():
    return {
        "success": True,
        "credits": "WLZBI",
        "name": "WLZBI Music API",
        "version": "1.0.0",
        "status": "Online",
        "developer": "WLZBI",
        "docs": "/docs",
        "endpoints": {
            "search": "/search?q=song_name",
            "play": "/play?q=song_name",
            "stream": "/stream?id=video_id",
            "download": "/download?id=video_id_or_song_name",
            "download_by_name": "/download?q=song_name",
            "song": "/song?id=video_id",
            "health": "/health"
        }
    }