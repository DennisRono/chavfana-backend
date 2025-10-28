from __future__ import annotations

import uuid
from datetime import date
from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import ForeignKey, Index, String, Date, Float, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from chavfana.models.base import BaseModel

if TYPE_CHECKING:
    from chavfana.models.farm import Farm
    from chavfana.models.user import User
    from chavfana.models.plot import Plot
    from chavfana.models.species import CropSpecies
    from chavfana.models.animal import AnimalGroup, Animal


class Project(BaseModel):
    __tablename__ = "projects"
    __table_args__ = (
        Index("ix_projects_farm_id", "farm_id"),
        Index("ix_projects_owner_id", "owner_id"),
        Index("ix_projects_status", "status"),
        Index("ix_projects_farm_status", "farm_id", "status"),
    )

    farm_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("farms.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
    )
    plot_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("plots.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
    )
    owner_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    project_type: Mapped[str] = mapped_column(
        String(50), nullable=False, comment="PlantingProject, AnimalKeepingProject"
    )
    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="Planning",
        index=True,
        comment="Planning, Active, Completed, Archived",
    )
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    notes: Mapped[Optional[str]] = mapped_column(String(2048), nullable=True)

    farm: Mapped["Farm"] = relationship("Farm", back_populates="projects")
    owner: Mapped["User"] = relationship("User", back_populates="projects")

    __mapper_args__ = {
        "polymorphic_identity": "Project",
        "polymorphic_on": project_type,
    }

    def __repr__(self) -> str:
        return f"<Project(id={self.id}, name={self.name}, type={self.project_type})>"


class PlantingProject(Project):
    __tablename__ = "planting_projects"
    __table_args__ = (Index("ix_planting_projects_project_id", "project_id"),)

    project_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("projects.id", ondelete="CASCADE"),
        primary_key=True,
    )
    species_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), nullable=True
    )
    expected_yield: Mapped[Optional[float]] = mapped_column(nullable=True)
    yield_unit: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    expected_revenue: Mapped[Optional[float]] = mapped_column(nullable=True)
    irrigation_type: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    soil_analysis_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), nullable=True
    )

    planting_events: Mapped[List["PlantingEvent"]] = relationship(
        "PlantingEvent", back_populates="project", cascade="all, delete-orphan"
    )

    __mapper_args__ = {
        "polymorphic_identity": "PlantingProject",
    }

    def __repr__(self) -> str:
        return f"<PlantingProject(id={self.project_id}, name={self.name})>"


class PlantingEvent(BaseModel):
    __tablename__ = "planting_events"
    __table_args__ = (
        Index("ix_planting_events_project_id", "project_id"),
        Index("ix_planting_events_plot_id", "plot_id"),
        Index("ix_planting_events_planting_date", "planting_date"),
    )

    project_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("planting_projects.project_id", ondelete="CASCADE"),
        primary_key=True,
    )

    plot_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), nullable=False, index=True
    )
    planting_date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    end_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    area_size: Mapped[float] = mapped_column(Float, nullable=False)
    area_unit: Mapped[str] = mapped_column(String(20), default="HECTARE")
    stage: Mapped[str] = mapped_column(
        String(50),
        default="Seedling",
        comment="Seedling, Vegetative, Flowering, Fruiting, Mature",
    )
    notes: Mapped[Optional[str]] = mapped_column(String(1024), nullable=True)
    species_details: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)

    project: Mapped["PlantingProject"] = relationship(
        "PlantingProject", back_populates="planting_events"
    )

    def __repr__(self) -> str:
        return f"<PlantingEvent(id={self.id}, project_id={self.project_id})>"


class AnimalKeepingProject(Project):
    __tablename__ = "animal_keeping_projects"
    __table_args__ = (Index("ix_animal_keeping_projects_project_id", "project_id"),)

    project_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("projects.id", ondelete="CASCADE"),
        primary_key=True,
    )
    housing_type: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    pasture_info: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    carrying_capacity: Mapped[Optional[int]] = mapped_column(nullable=True)

    animal_groups: Mapped[List["AnimalGroup"]] = relationship(
        "AnimalGroup", back_populates="project", cascade="all, delete-orphan"
    )
    individual_animals: Mapped[List["Animal"]] = relationship(
        "Animal", back_populates="project", cascade="all, delete-orphan"
    )

    __mapper_args__ = {
        "polymorphic_identity": "AnimalKeepingProject",
    }

    def __repr__(self) -> str:
        return f"<AnimalKeepingProject(id={self.project_id}, name={self.name})>"
