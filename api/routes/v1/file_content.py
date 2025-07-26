import time
from fastapi import APIRouter, UploadFile, File, Depends
from fastapi.concurrency import run_in_threadpool

from purrfectmeow import Malet
from ...loggings import setup_logger
from ...models.v1 import ResponseTemplate, FileContentForm

router = APIRouter()
logger = setup_logger(__name__)

@router.post('/file_content', response_model=ResponseTemplate)
async def file_content(
    file: UploadFile = File(...),
    form_data: FileContentForm = Depends()
):
    start = time.time()
    logger.info("Starting file content extraction...")
    try:
        content = await run_in_threadpool(
            Malet.loader,
            file.file,
            file.filename,
            form_data.file_loader
        )

        duration = time.time() - start
        logger.info(f"File content extraction completed successfully in {duration:.2f} seconds.")
        return ResponseTemplate(
            success=True,
            message="File Content Extraction Successfully.",
            data=content,
            time=duration
        )
    except Exception as e:
        duration = time.time() - start
        logger.error(
            f"File Content Extraction failed after {duration:.2f} seconds. "
            f"Error: {str(e)}"
        )
        return ResponseTemplate(
            success=False,
            message="File Content Extraction Failed.",
            data=str(e),
            time=duration
        )