"""Pydantic v2 schemas: validate data entering and leaving the API."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator

# --------------------------------------------------------------------------- #
# Tasks
# --------------------------------------------------------------------------- #


class TaskBase(BaseModel):
    # This common shape prevents create and response schemas from drifting.
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    priority: str = Field("medium", pattern="^(low|medium|high)$")


class TaskCreate(TaskBase):
    # This request schema intentionally omits id, timestamps, and is_completed.
    # Those are server-owned values a client must not choose when creating work.
    # Optional so the reference app is usable without first creating a project.
    project_id: Optional[int] = None

    @field_validator("title")
    @classmethod
    def title_must_not_be_whitespace(cls, v: str) -> str:
        # ``min_length`` accepts "   "; business validation rejects that case.
        if not v.strip():
            raise ValueError("Title cannot be empty or whitespace")
        return v.strip()


class TaskUpdate(BaseModel):
    # Every field is optional because PUT here supports a partial update.
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    is_completed: Optional[bool] = None
    priority: Optional[str] = Field(None, pattern="^(low|medium|high)$")


class TaskRead(TaskBase):
    # This response schema exposes server-generated fields, unlike TaskCreate.
    id: int
    is_completed: bool
    project_id: Optional[int] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    # Let FastAPI read attributes from a SQLAlchemy Task, not only a dict.
    model_config = ConfigDict(from_attributes=True)


# Alias kept because lessons 06/08/09 refer to the response schema as ``Task``.
Task = TaskRead


# --------------------------------------------------------------------------- #
# Projects
# --------------------------------------------------------------------------- #


class ProjectBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)


class ProjectCreate(ProjectBase):
    pass


class ProjectRead(ProjectBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


# --------------------------------------------------------------------------- #
# Users and auth
# --------------------------------------------------------------------------- #


class UserCreate(BaseModel):
    # Password is accepted on input only; UserRead below never returns it or its hash.
    email: str = Field(..., min_length=3, max_length=255)
    password: str = Field(..., min_length=8, max_length=128)


class UserRead(BaseModel):
    id: int
    email: str
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    # Matches OAuth2's conventional bearer-token response shape.
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    email: Optional[str] = None
