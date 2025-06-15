from fastapi import Form
from pydantic import BaseModel
from typing import Optional, Literal, List

class PreviewChunkingForm(BaseModel):
    embedding_model: Optional[str] = Form(default="text-embedding-3-large")
    file_reader: Optional[Literal["simple", "ocr", "markdown"]] = Form(default="simple")
    extra_params: Optional[str] = Form(default=None)

class PreviewChunkingResponse(BaseModel):
    success: bool
    message: str
    data: List[dict]
    time: float