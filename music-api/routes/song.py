from fastapi import APIRouter, HTTPException, Query

from services.extractor import extractor
from services.utils import format_duration

router = APIRouter(
    prefix="/song",
    tags=["Song"]
)


@router.get("")
async def song(
    id: str = Query(..., description="YouTube Video ID")
):

    try:

        data = await extractor.get_stream(id)

        data["duration_formatted"] = format_duration(
            data["duration"]
        )

        return {
            "success": True,
            "credits": "WLZBI",
            "result": data
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )