import time
from purrfectmeow import Malet, Suphalaks
from fastapi import APIRouter, UploadFile
from fastapi.concurrency import run_in_threadpool

from ...models import ResponseTemplate
from ...loggings import setup_logger

router = APIRouter()
logger = setup_logger(__name__)

@router.post('/file_reading')
async def file_reading(
    file: UploadFile, 
    loader: str = "PYMUPDF"
):
    start = time.time()
    logger.info(f"Received file '{file.filename}' for reading with loader '{loader}'.")
    try:
        file_path = await run_in_threadpool(Suphalaks.save_file, file.file, file.filename)
        metadata = await run_in_threadpool(Suphalaks.get_file_metadata, file_path)
        await run_in_threadpool(Suphalaks.remove_file, file_path)
        file.file.seek(0)
        
        content = await run_in_threadpool(
            Malet.loader, 
            file.file, 
            file.filename, 
            loader
        )
        data = {
            "file_content": content,
            "file_metadata": metadata
        }
        duration = time.time() - start
        logger.info(f"Successfully read file '{file.filename}' in {duration:.2f} seconds.")
        return ResponseTemplate(
            success=True,
            message="File Reading Successfully.",
            data=data,
            time=duration
        )
    except Exception as e:
        duration = time.time() - start
        logger.error(
            f"Failed to read file '{file.filename}' in {duration:.2f} seconds. "
            f"Error: {str(e)}"
        )
        return ResponseTemplate(
            success=False,
            message="File Reading Failed.",
            data=str(e),
            time=duration
        )
