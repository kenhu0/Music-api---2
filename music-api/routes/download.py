from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import FileResponse

from services.downloader import downloader

router = APIRouter(
    prefix="/download",
    tags=["Download"]
)


@router.get("")
async def download(
    id: str | None = Query(
        None,
        min_length=1,
        description="YouTube video ID, or a song name to search"
    ),
    q: str | None = Query(
        None,
        min_length=1,
        description="Song name to search for on YouTube"
    )
):
    if id is not None and q is not None:
        raise HTTPException(
            status_code=400,
            detail="Pass either 'id' or 'q', not both."
        )
    if id is None and q is None:
        raise HTTPException(
            status_code=400,
            detail="Provide a YouTube video ID with 'id' or a song name with 'q'."
        )

    try:
        data = await downloader.download(q if q is not None else id, search=q is not None)

        return FileResponse(
            path=data["filename"],
            filename=f"{data['title']}.mp3",
            media_type="audio/mpeg"
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )