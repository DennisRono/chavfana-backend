from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import Index, String

from chavfana.models.base import BaseModel
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from chavfana.models.project import PlantingEvent


class CropSpecies(BaseModel):
    __tablename__ = "crop_species"
    __table_args__ = (Index("ix_crop_species_name", "name"),)

    name: Mapped[str] = mapped_column(String(200), nullable=False, index=True)
    variety: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    species_type: Mapped[str] = mapped_column(
        String(50), nullable=False, comment="VEGETABLE, CEREAL, FRUIT, LEGUME, etc."
    )
    bloom_season: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    notes: Mapped[Optional[str]] = mapped_column(String(1024), nullable=True)

    def __repr__(self) -> str:
        return f"<CropSpecies(id={self.id}, name={self.name}, variety={self.variety})>"
