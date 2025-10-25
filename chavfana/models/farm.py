from __future__ import annotations

import uuid
from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import Index, String, Float, JSON, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from chavfana.models.base import BaseModel

if TYPE_CHECKING:
    from chavfana.models.user import User
    from chavfana.models.plot import Plot
    from chavfana.models.project import Project


class Farm(BaseModel):
    __tablename__ = "farms"
    __table_args__ = (
        Index("ix_farms_owner_id", "owner_id"),
        Index("ix_farms_owner_name", "owner_id", "name"),
        Index("ix_farms_country", "country"),
    )

    owner_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    name: Mapped[str] = mapped_column(String(200), nullable=False, index=True)
    description: Mapped[Optional[str]] = mapped_column(String(1024), nullable=True)
    country: Mapped[str] = mapped_column(String(2), nullable=False, index=True)
    city: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    address: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    geo_coordinate: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    rectangle_boundary: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    area_size: Mapped[float] = mapped_column(Float, nullable=False)
    area_unit: Mapped[str] = mapped_column(String(20), default="HECTARE")
    time_zone: Mapped[str] = mapped_column(String(50), default="UTC")

    owner: Mapped["User"] = relationship(
        "User", back_populates="farms", foreign_keys=[owner_id]
    )
    plots: Mapped[List["Plot"]] = relationship(
        "Plot", back_populates="farm", cascade="all, delete-orphan"
    )
    projects: Mapped[List["Project"]] = relationship(
        "Project", back_populates="farm", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Farm(id={self.id}, name={self.name}, owner_id={self.owner_id})>"
