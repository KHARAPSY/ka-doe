import time
from fastapi import APIRouter, Depends
from bson import ObjectId

from app.core import setup_logger
from app.api.deps import get_current_user, kls_col

router = APIRouter()
ACTION = "List Knowledges"

_logger = setup_logger(ACTION)

@router.get('/list_knowledges', dependencies=[Depends(get_current_user)])
def list_knowledges():
    _logger.info(f"[START] {ACTION} requested")
    start = time.time()
    
    try:
        res = kls_col.find({}).sort('created_date', 1)

        kls = []
        for i in res:
            if isinstance(i.get('_id'), ObjectId):
                i['knowledge_id'] = str(i['_id'])
                del i['_id']

            if 'created_date' in i and hasattr(i['created_date'], 'strftime'):
                i['created_date'] = i['created_date'].strftime('%d/%m/%Y')
            kls.append(i)

        elapsed = time.time() - start
        _logger.info(f"[SUCCESS] {ACTION} completed in {elapsed:.2f}s")
        
        return {
            "success": True,
            "data": kls,
            "time": elapsed
        }
    except Exception as e:
        elapsed = time.time() - start
        _logger.info(f"[ERROR] {ACTION} failed in {elapsed:.2f}s | error={str(e)}")
        
        return {
            "success": False,
            "data": str(e),
            "time": elapsed
        }
