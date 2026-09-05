"""SQLAlchemy database models: the table definitions for TaskFlow."""

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from database import Base


class User(Base):
    # ``__tablename__`` maps this Python class to the physical ``users`` table.
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # ORM-level cascade complements the ForeignKey cascade below. Deleting a
    # User through SQLAlchemy also removes owned rows instead of orphaning them.
    tasks = relationship(
        "Task", back_populates="owner", cascade="all, delete-orphan"
    )
    projects = relationship(
        "Project", back_populates="owner", cascade="all, delete-orphan"
    )


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    description = Column(String(1000))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Database-level cascade also protects integrity if SQL bypasses the ORM.
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))

    owner = relationship("User", back_populates="projects")
    tasks = relationship(
        "Task", back_populates="project", cascade="all, delete-orphan"
    )


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False, index=True)
    description = Column(String(1000))
    is_completed = Column(Boolean, default=False, index=True)
    priority = Column(String(20), default="medium")
    due_date = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # A task belongs to its creator. The API supplies this value from the JWT,
    # rather than trusting a client to choose an arbitrary user_id in JSON.
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    # project_id remains optional so the introductory app can create tasks
    # before a user has created any projects.
    project_id = Column(Integer, ForeignKey("projects.id", ondelete="CASCADE"))

    # ``back_populates`` makes each relationship navigable in either direction:
    # ``task.owner`` and ``user.tasks`` describe the same association.
    owner = relationship("User", back_populates="tasks")
    project = relationship("Project", back_populates="tasks")
