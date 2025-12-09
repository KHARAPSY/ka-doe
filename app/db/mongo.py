from pymongo import MongoClient

from app.core import Settings

class MongoDBConnect:
    client = MongoClient(Settings.MONGO_URI)

    @classmethod
    def knowledges_collection(cls):
        return cls.client.knowledges
    
    @classmethod
    def knowledge_files_collection(cls):
        return cls.client.knowledge_files