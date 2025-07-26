from fastapi import APIRouter

from .file_metadata import router as route_01
from .file_content import router as route_02
from .file_chunking import router as route_03

router = APIRouter(
    prefix='/v1', 
    tags=['version 1']
)

router.include_router(route_01)
router.include_router(route_02)
router.include_router(route_03)