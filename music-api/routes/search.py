from fastapi import APIRouter, HTTPException, Query
from services.youtube import youtube

router = APIRouter(
    prefix="/search",
    tags=["Search"]
)


@router.get("")
async def search(
    q: str = Query(..., min_length=1, description="Song name"),
    limit: int = Query(10, ge=1, le=25)
):
    try:
        results = await youtube.search(q, limit)

        return {
            "success": True,
            "credits": "WLZBI",
            "query": q,
            "count": len(results),
            "results": results
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )