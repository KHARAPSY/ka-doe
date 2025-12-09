import time
from fastapi import APIRouter, Depends, File, UploadFile, Form
from purrfectmeow.meow.felis import MetaFile

from app.core import setup_logger
from app.api.deps import get_current_user, MinIOConnect, kl_fs_col

router = APIRouter()
ACTION = "Upload Knowledge Data"

_logger = setup_logger(ACTION)

@router.post('/upload_knowledge_data/{knowledge_id}', dependencies=[Depends(get_current_user)])
async def upload_knowledge_data(knowledge_id: str, file: UploadFile = File(...)):
    _logger.info(f"[START] {ACTION} requested")
    start = time.time()

    from io import BytesIO

    content = await file.read()
    metadata = MetaFile.get_metadata(BytesIO(content), file_name=file.filename)
    
    try:
        knowledge_data = kl_fs_col.find_one({"file_md5": metadata.get('file_md5')})
        if knowledge_data is None:
            metadata['knowledge_ids'] = [knowledge_id]
            kl_fs_col.insert_one(metadata).inserted_id

        else:
            if knowledge_id not in knowledge_data.get('knowledge_ids'):
                kl_fs_col.update_one(
                    {"file_md5": metadata.get('file_md5')},
                    {'$push': {'knowledge_ids': knowledge_id}}
                )
        
        file.file.seek(0)
        await MinIOConnect.upload_file(
            file=file,
            file_name=metadata.get('file_md5')
        )

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
