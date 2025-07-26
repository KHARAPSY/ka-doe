from fastapi import Form
from pydantic import BaseModel
from typing import Optional, Literal

class FileChunkingForm(BaseModel):
    text: str = Form(...)
    splitter: Literal['token', 'separate'] = Form('token')
    model_name: Optional[str] = Form("text-embedding-3-small")
    chunk_size: Optional[int] = Form(500)
    chunk_overlap: Optional[int] = Form(0)
    chunk_separator: Optional[str] = Form("\n\n")