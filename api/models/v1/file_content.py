from fastapi import Form
from pydantic import BaseModel
from typing import Optional

class FileContentForm(BaseModel):
    file_loader: Optional[str] = Form(default="PYMUPDF")
    kwargs: Optional[str] = Form(default=None)