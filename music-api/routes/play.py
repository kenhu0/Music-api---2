from fastapi import APIRouter, HTTPException, Query
from services.youtube import youtube
from services.extractor import extractor

router = APIRouter(
    prefix="/play",
    tags=["Play"]
)


@router.get("")
async def play(
    q: str = Query(..., min_length=1, description="Song name")
):
    try:

        results = await youtube.search(q, 1)

        if not results:
            raise HTTPException(
                status_code=404,
                detail="No songs found."
            )

        video = results[0]

        data = await extractor.get_stream(video["id"])

        return {
            "success": True,
            "credits": "WLZBI",
            "query": q,
            "result": data
        }

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )