"""Task API endpoints. Mounted at /api/v1/tasks."""

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

import models
import schemas
from api.deps import get_current_user, get_db
from services import task_service

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("/", response_model=List[schemas.TaskRead])
async def list_tasks(
    skip: int = 0,
    limit: int = 100,
    completed: Optional[bool] = None,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    if completed is not None:
        return task_service.get_tasks_by_status(db, completed, skip, limit)
    return task_service.get_tasks(db, skip, limit)


@router.post(
    "/", response_model=schemas.TaskRead, status_code=status.HTTP_201_CREATED
)
async def create_task(
    task: schemas.TaskCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    return task_service.create_task(db, task, user_id=current_user.id)


@router.get("/{task_id}", response_model=schemas.TaskRead)
async def get_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
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
    task = task_service.update_task(db, task_id, task_update)
    if task is None:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
    return task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    if not task_service.delete_task(db, task_id):
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
