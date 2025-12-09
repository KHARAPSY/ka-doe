from fastapi import APIRouter, Depends
from app.api.deps import get_current_user, get_task_result

router = APIRouter(prefix='/job_status')

@router.get("/{task_id}", dependencies=[Depends(get_current_user)])
async def check_status(task_id: str):
    """Check task status or get result if ready."""
    result = await get_task_result(task_id)
    if result is None:
        return {"status": "processing"}
    return {"status": "completed", "result": result}