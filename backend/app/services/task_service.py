"""Task business logic.

Module-level functions (not a class): route handlers call
``task_service.get_tasks(db, skip, limit)`` etc. Each function takes a ``Session``
so the service layer stays free of HTTP concerns.
"""

from typing import Optional

from sqlalchemy.orm import Session

import models
import schemas


def get_tasks(db: Session, skip: int = 0, limit: int = 100):
    # offset/limit implement simple pagination while keeping HTTP query parsing
    # in the route layer.
    return db.query(models.Task).offset(skip).limit(limit).all()


def get_tasks_by_status(
    db: Session, completed: bool, skip: int = 0, limit: int = 100
):
    return (
        db.query(models.Task)
        .filter(models.Task.is_completed == completed)
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_task(db: Session, task_id: int) -> Optional[models.Task]:
    return db.query(models.Task).filter(models.Task.id == task_id).first()


def create_task(
    db: Session, task: schemas.TaskCreate, user_id: Optional[int] = None
) -> models.Task:
    # SQLAlchemy stages the object, writes it at commit, then refreshes it so
    # database-generated fields such as id and timestamps are available to send.
    db_task = models.Task(**task.model_dump(), user_id=user_id)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def update_task(
    db: Session, task_id: int, task_update: schemas.TaskUpdate
) -> Optional[models.Task]:
    db_task = get_task(db, task_id)
    if db_task is None:
        return None
    # A partial request must change only supplied fields. Without exclude_unset,
    # Pydantic defaults/None values could erase data the client did not mention.
    for key, value in task_update.model_dump(exclude_unset=True).items():
        setattr(db_task, key, value)
    db.commit()
    db.refresh(db_task)
    return db_task


def delete_task(db: Session, task_id: int) -> bool:
    db_task = get_task(db, task_id)
    if db_task is None:
        return False
    # The ORM cascade rules in models.py clean up dependent rows as needed.
    db.delete(db_task)
    db.commit()
    return True
