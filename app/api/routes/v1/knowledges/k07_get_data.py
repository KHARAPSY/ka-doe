import time
from fastapi import APIRouter, Depends
from purrfectmeow import Suphalak
from io import BytesIO

from app.core import setup_logger
from app.api.deps import get_current_user, kl_fs_col, MinIOConnect, enqueue_task

router = APIRouter()
ACTION = "Get Knowledge Data"

_logger = setup_logger(ACTION)

@router.get('/get_knowledge_data/{knowledge_data_hash}', dependencies=[Depends(get_current_user)])
async def get_knowledge_data(knowledge_data_hash: str):
    _logger.info(f"[START] {ACTION} requested")
    start = time.time()
    
    try:
        res = kl_fs_col.find_one({'file_md5': knowledge_data_hash})

        res.pop('_id', None)
        res.pop('knowledge_ids', None)

        if not res.get('content'):
            file_obj = MinIOConnect.download_file(knowledge_data_hash)

            def load_file():
                return Suphalak.reading(BytesIO(file_obj.read()), res.get('file_name'))

            task_id = await enqueue_task(load_file)
            res['task_id'] = task_id
        else:
            res['task_id'] = 'completed'

        elapsed = time.time() - start
        _logger.info(f"[SUCCESS] {ACTION} completed in {elapsed:.2f}s")
        
        return {
            "success": True,
            "data": res,
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
