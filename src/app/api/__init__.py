from fastapi import APIRouter

from .auth import router as auth_router
from .leads_router import router as lead_router
from .tg_bot import router as bot_router

router = APIRouter()
router.include_router(auth_router)
router.include_router(lead_router)
router.include_router(bot_router)