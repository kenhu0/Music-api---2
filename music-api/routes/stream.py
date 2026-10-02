from fastapi import APIRouter, HTTPException, Query
from services.extractor import extractor

router = APIRouter(
    prefix="/stream",
    tags=["Streaming"]
)


@router.get("")
async def stream(
    id: str = Query(..., description="YouTube Video ID")
):
    try:

        data = await extractor.get_stream(id)

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
