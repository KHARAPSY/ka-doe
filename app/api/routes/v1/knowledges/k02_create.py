import time
from fastapi import APIRouter, Depends

from app.core import setup_logger
from app.schemas import NewKnowledgeForm
from app.api.deps import get_current_user, kls_col

router = APIRouter()
ACTION = "Create Knowledge"

_logger = setup_logger(ACTION)

@router.post('/create_knowledge', dependencies=[Depends(get_current_user)])
def create_knowledge(form_data: NewKnowledgeForm):
    _logger.info(f"[START] {ACTION} requested")
    start = time.time()
    
    try:
        kls_col.insert_one(form_data.dict()).inserted_id

        elapsed = time.time() - start
        _logger.info(f"[SUCCESS] {ACTION} completed in {elapsed:.2f}s")
        
        return {
            "success": True,
            "data": "Knowledge created successfully.",
            "time": elapsed
        }
    except Exception as e:
        elapsed = time.time() - start
        _logger.info(f"[ERROR] {ACTION} failed in {elapsed:.2f}s | error={str(e)}")
        
        return {
            "success": False,
            "data": str(e),
            "time": elapsed
        }
