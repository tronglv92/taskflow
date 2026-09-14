"""Task API endpoints. Mounted at /api/v1/tasks."""

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

import models
import schemas
from api.deps import get_current_user, get_db
from services import task_service
from services import redis_cache

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("/", response_model=List[schemas.TaskRead])
async def list_tasks(
    skip: int = 0,
    limit: int = 100,
    completed: Optional[bool] = None,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    # Dependency resolution happens before this function body. The reference
    # app currently authenticates all callers but does not yet scope this list
    # to ``current_user``; that simplification is intentional for the lab.
    cache_key = f"taskflow:tasks:{completed}:{skip}:{limit}"
    cached = redis_cache.get_json(cache_key)
    if cached is not None:
        return cached
    if completed is not None:
        tasks = task_service.get_tasks_by_status(db, completed, skip, limit)
    else:
        tasks = task_service.get_tasks(db, skip, limit)
    payload = [
        schemas.TaskRead.model_validate(task).model_dump(mode="json") for task in tasks
    ]
    redis_cache.set_json(cache_key, payload)
    return payload


@router.post("/", response_model=schemas.TaskRead, status_code=status.HTTP_201_CREATED)
async def create_task(
    task: schemas.TaskCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    # The authenticated identity, rather than the request schema, determines
    # task ownership and prevents a caller from assigning a task to someone else.
    created = task_service.create_task(db, task, user_id=current_user.id)
    redis_cache.invalidate_pattern("taskflow:tasks:*")
    return created


@router.get("/{task_id}", response_model=schemas.TaskRead)
async def get_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    # The service returns None for an absent row; routes translate that domain
    # result into the HTTP-specific 404 response.
    task = task_service.get_task(db, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
    return task


@router.put("/{task_id}", response_model=schemas.TaskRead)
async def update_task(
    task_id: int,
    task_update: schemas.TaskUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    # ``exclude_unset`` in the service means a body with only is_completed does
    # not overwrite title, description, or priority with their default values.
    task = task_service.update_task(db, task_id, task_update)
    if task is None:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
    redis_cache.invalidate_pattern("taskflow:tasks:*")
    return task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    if not task_service.delete_task(db, task_id):
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
    redis_cache.invalidate_pattern("taskflow:tasks:*")
