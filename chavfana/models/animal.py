from __future__ import annotations

import uuid
from datetime import date, datetime
from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import Index, String, Float, Integer, Date, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from chavfana.models.base import BaseModel

if TYPE_CHECKING:
    from chavfana.models.project import AnimalKeepingProject
    from chavfana.models.veterinary import VeterinaryVisit


class AnimalGroup(BaseModel):
    __tablename__ = "animal_groups"
    __table_args__ = (
        Index("ix_animal_groups_project_id", "project_id"),
        Index("ix_animal_groups_housing", "housing"),
    )

    project_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("animal_keeping_projects.project_id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    group_name: Mapped[str] = mapped_column(String(200), nullable=False)
    housing: Mapped[str] = mapped_column(
        String(100), nullable=False, comment="Pasture, Barn, Coop, Pen, etc."
    )
    starting_number: Mapped[int] = mapped_column(Integer, nullable=False)
    average_weight: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    average_age: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    disease_alerts: Mapped[bool] = mapped_column(default=False)
    quarantine_info: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    notes: Mapped[Optional[str]] = mapped_column(String(1024), nullable=True)

    project: Mapped["AnimalKeepingProject"] = relationship(
        "AnimalKeepingProject", back_populates="animal_groups"
    )
    animals: Mapped[List["Animal"]] = relationship(
        "Animal", back_populates="group", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<AnimalGroup(id={self.id}, group_name={self.group_name})>"


class Animal(BaseModel):
    __tablename__ = "animals"
    __table_args__ = (
        Index("ix_animals_project_id", "project_id"),
        Index("ix_animals_group_id", "group_id"),
        Index("ix_animals_tag", "tag"),
        Index("ix_animals_is_active", "is_active"),
    )

    project_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("animal_keeping_projects.project_id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    group_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("animal_groups.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    tag: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    breed: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    name: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    arrival_date: Mapped[date] = mapped_column(Date, nullable=False)
    birthday: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    animal_type: Mapped[str] = mapped_column(
        String(50), nullable=False, comment="Cattle, Sheep, Goat, Pig, Chicken, etc."
    )
    gender: Mapped[str] = mapped_column(String(20), nullable=False)
    weight: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    age_estimate: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    is_active: Mapped[bool] = mapped_column(default=True, index=True)
    health_status: Mapped[str] = mapped_column(
        String(50), default="Healthy", comment="Healthy, Sick, Recovering, Quarantined"
    )
    insurance_policy: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)

    project: Mapped["AnimalKeepingProject"] = relationship(
        "AnimalKeepingProject", back_populates="individual_animals"
    )
    group: Mapped[Optional["AnimalGroup"]] = relationship(
        "AnimalGroup", back_populates="animals"
    )
    veterinary_visits: Mapped[List["VeterinaryVisit"]] = relationship(
        "VeterinaryVisit", back_populates="animal", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Animal(id={self.id}, tag={self.tag}, animal_type={self.animal_type})>"
