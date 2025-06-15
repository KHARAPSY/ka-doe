from pydantic import BaseModel
from typing import Any, Optional, Union

class ResponseTemplate(BaseModel):
    success: bool
    message: str
    data: Optional[Any] = None
    time: Union[str, float]