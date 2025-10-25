from __future__ import annotations

import uuid
from datetime import date, datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy import Index, String, Integer, Date, DateTime, JSON, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from chavfana.models.base import BaseModel

if TYPE_CHECKING:
    from .farm import Farm, Plot
    from .project import Project
    from .user import User


class DailyEntry(BaseModel):
    __tablename__ = "daily_entries"
    __table_args__ = (
        Index("ix_daily_entries_farm_id", "farm_id"),
        Index("ix_daily_entries_date", "date"),
        Index("ix_daily_entries_farm_date", "farm_id", "date"),
    )

    farm_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("farms.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    author_user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    project_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("projects.id", ondelete="SET NULL"),
        nullable=True,
    )
    plot_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("plots.id", ondelete="SET NULL"),
        nullable=True,
    )
    entry_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        comment="Activity, Note, Expense, Observation",
    )
    content: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    duration_minutes: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    cost: Mapped[Optional[float]] = mapped_column(nullable=True)
    currency: Mapped[str] = mapped_column(String(3), default="USD")

    def __repr__(self) -> str:
        return f"<DailyEntry(id={self.id}, farm_id={self.farm_id}, date={self.date})>"


class Task(BaseModel):
    __tablename__ = "tasks"
    __table_args__ = (
        Index("ix_tasks_assigned_to_id", "assigned_to_id"),
        Index("ix_tasks_project_id", "project_id"),
        Index("ix_tasks_status", "status"),
        Index("ix_tasks_due_date", "due_date"),
    )

    assigned_to_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    project_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("projects.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String(1024), nullable=True)
    due_date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    completed_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    status: Mapped[str] = mapped_column(
        String(50), default="Pending", comment="Pending, In Progress, Completed, Cancelled"
    )
    priority: Mapped[str] = mapped_column(
        String(20), default="Medium", comment="Low, Medium, High, Critical"
    )
    notes: Mapped[Optional[str]] = mapped_column(String(1024), nullable=True)

    def __repr__(self) -> str:
        return f"<Task(id={self.id}, title={self.title}, status={self.status})>"
