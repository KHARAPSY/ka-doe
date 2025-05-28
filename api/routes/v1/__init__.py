from fastapi import APIRouter

from .file_reading import router as file_reading_route
from .preview_chunking import router as preview_chunking_route
from .document_forming import router as document_forming_route

router = APIRouter(
    prefix='/v1', 
    tags=['version 1']
)

router.include_router(file_reading_route)
router.include_router(preview_chunking_route)
router.include_router(document_forming_route)