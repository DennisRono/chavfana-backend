from __future__ import annotations

import uuid
from datetime import datetime
from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import Index, String, Boolean, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from chavfana.models.base import BaseModel

if TYPE_CHECKING:
    from chavfana.models.farm import Farm
    from chavfana.models.project import Project
    from chavfana.models.veterinary import VeterinaryVisit


class User(BaseModel):
    __tablename__ = "users"
    __table_args__ = (
        Index("ix_users_email", "email", unique=True),
        Index("ix_users_role", "role"),
        Index("ix_users_is_active", "is_active"),
    )

    email: Mapped[str] = mapped_column(
        String(255), nullable=False, unique=True, index=True
    )
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    phone: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    role: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="FARMER",
        comment="ADMIN, FARMER, MANAGER, EMPLOYEE, VET, AGRONOMIST, CONSULTANT",
    )
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    last_login: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    profile_data: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)

    farms: Mapped[List["Farm"]] = relationship(
        "Farm", back_populates="owner", foreign_keys="Farm.owner_id"
    )
    projects: Mapped[List["Project"]] = relationship(
        "Project", back_populates="owner", foreign_keys="Project.owner_id"
    )
    veterinary_visits: Mapped[List["VeterinaryVisit"]] = relationship(
        "VeterinaryVisit", back_populates="vet", foreign_keys="VeterinaryVisit.vet_id"
    )

    def __repr__(self) -> str:
        return f"<User(id={self.id}, email={self.email}, role={self.role})>"


class Employee(BaseModel):

    __tablename__ = "employees"
    __table_args__ = (
        Index("ix_employees_user_id", "user_id", unique=True),
        Index("ix_employees_farm_id", "farm_id"),
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    farm_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("farms.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    position: Mapped[str] = mapped_column(String(100), nullable=False)
    employment_start: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    employment_end: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    salary_amount: Mapped[Optional[float]] = mapped_column(nullable=True)
    salary_currency: Mapped[str] = mapped_column(String(3), default="USD")

    def __repr__(self) -> str:
        return f"<Employee(user_id={self.user_id}, position={self.position})>"
