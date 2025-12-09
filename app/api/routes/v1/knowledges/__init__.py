from fastapi import APIRouter

from .k01_list import router as route_01
from .k02_create import router as route_02
from .k03_delete import router as route_03
from .k04_profile import router as route_04
from .k05_upload_data import router as route_05
from .k06_remove_data import router as route_06
from .k07_get_data import router as route_07
from .k08_dowload_data import router as route_08
from .k09_save_content import router as route_09
from .k10_read_content import router as route_10

router = APIRouter(prefix='/knowledges')

router.include_router(route_01)
router.include_router(route_02)
router.include_router(route_03)
router.include_router(route_04)
router.include_router(route_05)
router.include_router(route_06)
router.include_router(route_07)
router.include_router(route_08)
router.include_router(route_09)
router.include_router(route_10)
