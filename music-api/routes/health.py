from fastapi import APIRouter
from datetime import datetime

router = APIRouter(
    prefix="/health",
    tags=["Health"]
)


@router.get("")
async def health():
    return {
        "success": True,
        "credits": "WLZBI",
        "status": "online",
        "api": "WLZBI Music API",
        "version": "1.0.0",
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }