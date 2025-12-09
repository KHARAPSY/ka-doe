from fastapi import APIRouter

from .routes import router as routes

router = APIRouter()

router.include_router(routes)
