from fastapi import APIRouter

from .knowledges import router as route_knowledges

router = APIRouter(prefix='/v1', tags=['Version 1'])

router.include_router(route_knowledges)
