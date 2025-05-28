import time
from purrfectmeow import Kornja
from fastapi import APIRouter
from fastapi.concurrency import run_in_threadpool

from ...models import ResponseTemplate
from ...loggings import setup_logger

router = APIRouter()
logger = setup_logger(__name__)

@router.post('/preview_chunking')
async def preview_chunking(
    text: str,
    splitter: str,
    embedding_model: str,
    chunk_size: int,
    chunk_overlap: int,
):
    start = time.time()
    logger.info(
        f"Starting preview chunking using model='{embedding_model}', "
        f"splitter='{splitter}', chunk_size={chunk_size}, chunk_overlap={chunk_overlap}."
    )
    try:
        chunks = await run_in_threadpool(
            Kornja.chunking,
            text, 
            splitter, 
            kwargs={
                "model_name": embedding_model,
                "chunk_size": chunk_size,
                "chunk_overlap": chunk_overlap
            }
        )
        duration = time.time() - start
        logger.info(
            f"Successfully chunked preview text into {len(chunks)} chunks in {duration:.2f} seconds."
        )
        return ResponseTemplate(
            success=True,
            message="Preview Chunking Successfully.",
            data=chunks,
            time=duration
        )
    except Exception as e:
        duration = time.time() - start
        logger.error(
            f"Preview chunking failed after {duration:.2f} seconds. "
            f"Error: {str(e)}"
        )
        return ResponseTemplate(
            success=False,
            message="Preview Chunking Failed.",
            data=str(e),
            time=duration
        )