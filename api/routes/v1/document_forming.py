import time
from typing import List, Dict, Any
from purrfectmeow import Suphalaks
from fastapi import APIRouter
from fastapi.concurrency import run_in_threadpool

from ...models import ResponseTemplate
from ...loggings import setup_logger

router = APIRouter()
logger = setup_logger(__name__)

@router.post('/document_forming')
async def document_forming(
    chunks: List[str],
    metadata: Dict[str, Any]
):
    start = time.time()
    logger.info(f"Document forming started with {len(chunks)} chunks and metadata keys: {list(metadata.keys())}")
    try:
        docs = await run_in_threadpool(
            Suphalaks.document_template,
            chunks, 
            metadata
        )
        duration = time.time() - start
        logger.info(f"Document forming completed successfully in {duration:.2f} seconds.")
        return ResponseTemplate(
            success=True,
            message="Document Forming Successfully.",
            data=docs,
            time=duration
        )
    except Exception as e:
        duration = time.time() - start
        logger.error(
            f"Document Forming failed after {duration:.2f} seconds. "
            f"Error: {str(e)}"
        )
        return ResponseTemplate(
            success=False,
            message="Document Forming Failed.",
            data=str(e),
            time=duration
        )