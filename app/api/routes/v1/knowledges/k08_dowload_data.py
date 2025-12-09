import time
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from urllib.parse import quote

from app.core import setup_logger
from app.api.deps import get_current_user, MinIOConnect, kl_fs_col

router = APIRouter()
ACTION = "Download Knowledge Data"

_logger = setup_logger(ACTION)

@router.get('/download_knowledge_data/{knowledge_data_hash}', dependencies=[Depends(get_current_user)])
def download_knowledge_data(knowledge_data_hash: str):
    _logger.info(f"[START] {ACTION} requested")
    start = time.time()

    try:
        res = kl_fs_col.find_one({'file_md5': knowledge_data_hash})
        res.pop('_id')
        res.pop('knowledge_ids')

        file_name = res.get('file_name')
        file_type = res.get('file_type')

        file_obj = MinIOConnect.download_file(knowledge_data_hash)
        content_disposition = f"attachment; filename={quote(file_name)}"

        elapsed = time.time() - start
        _logger.info(f"[SUCCESS] {ACTION} completed in {elapsed:.2f}s")
        
        return StreamingResponse(
            file_obj,
            media_type=file_type,
            headers={"Content-Disposition": content_disposition}
        )
    
    except Exception as e:
        elapsed = time.time() - start
        _logger.info(f"[ERROR] {ACTION} failed in {elapsed:.2f}s | error={str(e)}")
        
        raise HTTPException(status_code=404, detail=str(e))
