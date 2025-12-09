import torch
from fastapi import APIRouter

router = APIRouter(prefix='/health_check')

@router.get("/get_status", include_in_schema=False)
def get_status():
    try:
        device = "cuda" if torch.cuda.is_available() else "cpu"
        # simple tensor test
        x = torch.tensor([1.0, 2.0], device=device)
        y = x * 2
        return {
            "status": "ok",
            "torch_version": torch.__version__,
            "device": device,
            "tensor_test": y.tolist()
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }
