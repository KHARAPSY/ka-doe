import os
import time
from fastapi import APIRouter, UploadFile, File
from fastapi.concurrency import run_in_threadpool
from purrfectmeow import Suphalaks
from ...loggings import setup_logger
from ...models.v1 import ResponseTemplate

router = APIRouter()
logger = setup_logger(__name__)

@router.post('/file_metadata', response_model=ResponseTemplate)
async def file_metadata(
    file: UploadFile = File(...)
):
    start = time.time()
    logger.info("Starting file metadata extraction...")
    try:
        if not os.path.exists(".cache/tmp_files"):
            os.makedirs(".cache/tmp_files")
            logger.info("Created directory: .cache/tmp_files")

        file_path = f".cache/tmp_files/{file.filename}"
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
            logger.info(f"File {file.filename} saved to {file_path}")

        metadata = await run_in_threadpool(
            Suphalaks.get_file_metadata,
            file_path
        )

        if os.path.exists(file_path):
            os.remove(file_path)
            logger.info(f"Temporary file {file_path} removed.")
        
        duration = time.time() - start
        logger.info(f"File metadata extraction completed successfully in {duration:.2f} seconds.")
        return ResponseTemplate(
            success=True,
            message="File Metadata Extraction Successfully.",
            data=metadata,
            time=duration
        )
    except Exception as e:
        duration = time.time() - start
        logger.error(
            f"File Metadata Extraction failed after {duration:.2f} seconds. "
            f"Error: {str(e)}"
        )
        return ResponseTemplate(
            success=False,
            message="File Metadata Extraction Failed.",
            data=str(e),
            time=duration
        )