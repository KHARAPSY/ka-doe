import time
import hashlib
from fastapi import APIRouter, Depends

from app.core import setup_logger
from app.api.deps import get_current_user, tasks, kl_fs_col, MinIOConnect

router = APIRouter()
ACTION = "Save Knowledge Data"

_logger = setup_logger(ACTION)

@router.post('/save_knowledge_content/{knowledge_data_hash}/{task_id}',dependencies=[Depends(get_current_user)])
async def save_knowledge_content(knowledge_data_hash: str, task_id: str):
    _logger.info(f"[START] {ACTION} requested")
    start = time.time()
    
    try:
        task_data = tasks.get(task_id)
        if not task_data:
            return None
        
        result = task_data["future"].result()

        if result:
            if not isinstance(result, str):
                result = str(result)

            file_name = hashlib.md5(result.encode("utf-8")).hexdigest()

            MinIOConnect.upload_read_file(result, file_name)

            kl_fs_col.update_one(
                {'file_md5': knowledge_data_hash},
                {'$set': {
                    'content': True,
                    'content_files': {
                        'default': file_name
                    }
                }}
            )
        else:
            kl_fs_col.update_one(
                {'file_md5': knowledge_data_hash},
                {'$set': {'content': False}}
            )

            elapsed = time.time() - start
            
        _logger.info(f"[SUCCESS] {ACTION} completed in {elapsed:.2f}s")
        
        return {
            "success": True,
            "data": "Data Saved.",
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
