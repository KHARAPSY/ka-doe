import time
from fastapi import APIRouter, Depends
from bson import ObjectId

from app.core import setup_logger
from app.api.deps import get_current_user, kl_fs_col, kls_col

router = APIRouter()
ACTION = "Knowledge Profile"

_logger = setup_logger(ACTION)

@router.get('/knowledge_profile/{knowledge_id}', dependencies=[Depends(get_current_user)])
def knowledge_profile(knowledge_id: str):
    _logger.info(f"[START] {ACTION} requested")
    start = time.time()
    
    try:
        res = kl_fs_col.find({"knowledge_ids": {'$in': [knowledge_id]}})
        
        kl_profile = []
        for i in res:
            if isinstance(i.get('_id'), ObjectId):
                i['knowledge_data_id'] = str(i['_id'])
                del i['_id']
                del i['knowledge_ids']

            kl_profile.append(i)

        data = [{
            {
                'file_name': 'knowledge_file',
                'file_md5': 'id'
            }[d]: k[d] for d in ['file_name', 'file_md5']
        } for k in kl_profile]

        kls = kls_col.find_one({'_id': ObjectId(knowledge_id)})

        kls.pop('_id')
        data.append(kls)

        elapsed = time.time() - start
        _logger.info(f"[SUCCESS] {ACTION} completed in {elapsed:.2f}s")
        
        return {
            "success": True,
            "data": data,
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
