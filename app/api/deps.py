# User

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated, Callable, Dict

from app.schemas import User
from app.core import setup_logger, AuthToken
from app.services import ServiceUser

oauth_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/token/login")
_logger = setup_logger("API Dependencies")

async def get_current_user(token: Annotated[str, Depends(oauth_scheme)]) -> User:
    _logger.debug("Attempting to decode access token.")
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = AuthToken.decode_access_token(token)
        _logger.debug(f"Decoded payload")
    except Exception as e:
        _logger.error(f"Error decoding token: {e}")
        raise credentials_exception

    if payload is None or (username := payload.get("sub")) is None:
        _logger.warning("Token payload is missing 'sub' (username).")
        raise credentials_exception

    _logger.debug(f"Fetching username `{username}`")
    user = ServiceUser.get_user(username)

    if user is None:
        _logger.warning(f"`{username}` username is not found.")
        raise credentials_exception

    _logger.debug(f"Authenticated `{user.username}` username")
    return user

async def get_admin_user(current_user: Annotated[User, Depends(get_current_user)]) -> User:
    if not current_user.is_admin == True:
        raise HTTPException(status_code=400, detail="Not an admin account")
    return current_user

async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)]
) -> User:
    _logger.debug(f"Checking if `{current_user.username}` username is active")
    if current_user.disabled:
        _logger.warning(f"`{current_user.username}` username is inactive")
        raise HTTPException(status_code=400, detail="Inactive user")

    _logger.debug(f"`{current_user.username}` username is active")
    return current_user

# Databases

from app.db import MinIOConnect

s3 = MinIOConnect.s3
MinIOConnect.ensure_bucket()
MinIOConnect.ensure_folder()

from app.db import MongoDBConnect

kls_col = MongoDBConnect.knowledges_collection()
kl_fs_col = MongoDBConnect.knowledge_files_collection()

# Queue

import asyncio
import uuid
import time

task_queue = asyncio.Queue()
tasks: Dict[str, dict] = {}  # task_id -> {"future": Future, "created_at": float}

async def worker():
    """Background worker that processes queued tasks."""
    while True:
        task_id, func, args, kwargs = await task_queue.get()
        future = tasks[task_id]["future"]

        try:
            if asyncio.iscoroutinefunction(func):
                result = await func(*args, **kwargs)
            else:
                loop = asyncio.get_running_loop()
                result = await loop.run_in_executor(None, func, *args)
            future.set_result(result)
        except Exception as e:
            future.set_exception(e)
        finally:
            task_queue.task_done()

async def enqueue_task(func: Callable, *args, **kwargs) -> str:
    """Queue a task and return its task_id immediately."""
    task_id = str(uuid.uuid4())
    loop = asyncio.get_running_loop()
    future = loop.create_future()
    tasks[task_id] = {"future": future, "created_at": time.time()}
    await task_queue.put((task_id, func, args, kwargs))
    return task_id

async def get_task_result(task_id: str):
    """Retrieve task result if finished, or check status."""
    task_data = tasks.get(task_id)
    if not task_data:
        return None
    future = task_data["future"]
    if future.done():
        try:
            return future.result()
        except Exception as e:
            return str(e)
    return None

async def cleanup_tasks(max_age_seconds: int = 3600):
    """Periodically clean up completed/old tasks."""
    while True:
        now = time.time()
        to_delete = []
        for task_id, data in tasks.items():
            future = data["future"]
            if future.done() and (now - data["created_at"] > max_age_seconds):
                to_delete.append(task_id)
        for task_id in to_delete:
            del tasks[task_id]
        await asyncio.sleep(300)

async def init_workers(worker_count: int = 2):
    """Start workers and cleanup task."""
    for _ in range(worker_count):
        asyncio.create_task(worker())
    asyncio.create_task(cleanup_tasks())
    _logger.info(f"🚀 Started {worker_count} background worker(s) + cleanup scheduler.")
