import time
from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from urllib.parse import quote

from app.core import setup_logger
from app.api.deps import get_current_user, kl_fs_col, MinIOConnect

router = APIRouter()
ACTION = "Read Knowledge Data"

_logger = setup_logger(ACTION)

@router.get('/read_knowledge_content/{knowledge_data_hash}',dependencies=[Depends(get_current_user)])
def read_knowledge_content(knowledge_data_hash: str):
    _logger.info(f"[START] {ACTION} requested")
    start = time.time()
    
    try:
        content = kl_fs_col.find_one({'file_md5': knowledge_data_hash})
        if content.get('content'):
            default_content_name = content.get('content_files')['default']
            file_obj = MinIOConnect.download_read_file(default_content_name)

        content_disposition = f"attachment; filename={quote(default_content_name)}.txt"

        elapsed = time.time() - start
        _logger.info(f"[SUCCESS] {ACTION} completed in {elapsed:.2f}s")
        
        return StreamingResponse(
            file_obj,
            media_type='text/plain',
            headers={"Content-Disposition": content_disposition}
        )
    
    except Exception as e:
        elapsed = time.time() - start
        _logger.info(f"[ERROR] {ACTION} failed in {elapsed:.2f}s | error={str(e)}")
        
        return {
            "success": False,
            "data": str(e),
            "time": elapsed
        }
