from fastapi import APIRouter

from .token import router as route_token

router = APIRouter(
    prefix='/auth',
    tags=['Authenication Token']
)

router.include_router(route_token)
