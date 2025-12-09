from fastapi import APIRouter

from .auth import router as route_auth
from .health_check import router as route_health
from .job_status import router as route_job

from .v1 import router as route_v1

router = APIRouter(prefix='/api')

router.include_router(route_auth)
router.include_router(route_health)
router.include_router(route_job)

router.include_router(route_v1)
