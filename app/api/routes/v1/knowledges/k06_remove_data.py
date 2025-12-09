import time
from fastapi import APIRouter, Depends

from app.core import setup_logger
from app.api.deps import get_current_user, MinIOConnect, kl_fs_col

router = APIRouter()
ACTION = "Remove Knowledge Data"

_logger = setup_logger(ACTION)

@router.delete('/remove_knowledge_data/{knowledge_id}/{knowledge_data_hash}', dependencies=[Depends(get_current_user)])
def remove_knowledge_data(knowledge_id: str, knowledge_data_hash: str):
    _logger.info(f"[START] {ACTION} requested")
    start = time.time()
    
    try:
        kl_fs_col.update_one(
            {"file_md5": knowledge_data_hash},
            {"$pull": {'knowledge_ids': knowledge_id}}
        )

        kl_ids = kl_fs_col.find_one({"knowledge_ids": {"$size": 0}})

        if kl_ids:
            kl_fs_col.delete_one({'file_md5': knowledge_data_hash})

            MinIOConnect.delete_file(knowledge_data_hash)

        elapsed = time.time() - start
        _logger.info(f"[SUCCESS] {ACTION} completed in {elapsed:.2f}s")
        
        return {
            "success": True,
            "data": "Knowledge Data Uploaded.",
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
