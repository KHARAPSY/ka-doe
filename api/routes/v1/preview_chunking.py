import time
from fastapi import APIRouter, Depends, UploadFile, File

from ...loggings import setup_logger
from ...helpers.v1 import ChunkingProcessor
from ...models.v1 import ResponseTemplate, PreviewChunkingForm, PreviewChunkingResponse

router = APIRouter()
logger = setup_logger(__name__)

@router.post('/preview_chunking')
def preview_chunking(
    file: UploadFile = File(...),
    request: PreviewChunkingForm = Depends()
):
    start = time.time()
    
    try:
        logger.info(
            f"Received file '{file.filename}' for preview chunking "
            f"with embedding model '{request.embedding_model}' "
            f"with loader '{request.file_reader}' "
            f"and extra params '{request.extra_params}'."
        )
        chunks = ChunkingProcessor.process_preview(
            file.file,
            file.filename,
            request.file_reader,
            request.extra_params
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