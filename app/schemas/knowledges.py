from pydantic import BaseModel
from datetime import datetime

class NewKnowledgeForm(BaseModel):
    knowledge_owner: str
    knowledge_name: str
    knowledge_embedding_model: str
    created_date: datetime = datetime.now()
