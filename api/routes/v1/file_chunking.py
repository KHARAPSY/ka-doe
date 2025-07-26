import time
from fastapi import APIRouter

from purrfectmeow import Kornja
from ...loggings import setup_logger
from ...models.v1 import ResponseTemplate, FileChunkingForm

router = APIRouter()
logger = setup_logger(__name__)

@router.post('/file_chunking', response_model=ResponseTemplate)
def file_chunking(form_data: FileChunkingForm):
    start = time.time()
    logger.info("Starting file chunking...")
    try:
        match form_data.splitter:
            case 'token':
                chunks = Kornja.chunking(
                    form_data.text,
                    form_data.model_name,
                    form_data.splitter,
                    chunk_size = form_data.chunk_size,
                    chunk_overlap = form_data.chunk_overlap,
                )
            case 'separate':
                chunks = Kornja.chunking(
                    form_data.text,
                    form_data.splitter,
                    chunk_separator = form_data.chunk_separator,
                )
        
        duration = time.time() - start
        logger.info(f"File chunking completed successfully in {duration:.2f} seconds.")
        return ResponseTemplate(
            success=True,
            message="File Chunking Successfully.",
            data=chunks,
            time=duration
        )
    except Exception as e:
        duration = time.time() - start
        logger.error(
            f"File Chunking failed after {duration:.2f} seconds. "
            f"Error: {str(e)}"
        )
        return ResponseTemplate(
            success=False,
            message="File Chunking Failed.",
            data=str(e),
            time=duration
        )