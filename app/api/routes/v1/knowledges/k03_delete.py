import time
from fastapi import APIRouter, Depends
from bson import ObjectId

from app.core import setup_logger
from app.api.deps import get_current_user, kls_col

router = APIRouter()
ACTION = "Delete Knowledge"

_logger = setup_logger(ACTION)

@router.delete('/delete_knowledge/{knowledge_id}', dependencies=[Depends(get_current_user)])
def delete_knowledge(knowledge_id: str):
    _logger.info(f"[START] {ACTION} requested")
    start = time.time()
    
    try:
        kls_col.delete_one({"_id": ObjectId(knowledge_id)})

        elapsed = time.time() - start
        _logger.info(f"[SUCCESS] {ACTION} completed in {elapsed:.2f}s")
        
        return {
            "success": True,
            "data": "Knowledge deleted successfully.",
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
