from __future__ import annotations

import uuid
from typing import TYPE_CHECKING, Optional

from sqlalchemy import Index, String, Float, JSON, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from chavfana.models.base import BaseModel

if TYPE_CHECKING:
    from chavfana.models.farm import Farm


class Plot(BaseModel):
    __tablename__ = "plots"
    __table_args__ = (
        Index("ix_plots_farm_id", "farm_id"),
        Index("ix_plots_farm_plotcode", "farm_id", "plot_code", unique=True),
        Index("ix_plots_current_crop", "current_crop_id"),
    )

    farm_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("farms.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    plot_code: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    area_size: Mapped[float] = mapped_column(Float, nullable=False)
    area_unit: Mapped[str] = mapped_column(String(20), default="HECTARE")
    soil_profile: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    gps_bounds: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    current_crop_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), nullable=True, index=True
    )

    farm: Mapped["Farm"] = relationship("Farm", back_populates="plots")

    def __repr__(self) -> str:
        return f"<Plot(id={self.id}, plot_code={self.plot_code}, farm_id={self.farm_id})>"
