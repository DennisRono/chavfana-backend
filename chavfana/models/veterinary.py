from __future__ import annotations

import uuid
from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy import Index, String, Float, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from chavfana.models.base import BaseModel

if TYPE_CHECKING:
    from chavfana.models.animal import Animal
    from chavfana.models.user import User


class VeterinaryVisit(BaseModel):
    __tablename__ = "veterinary_visits"
    __table_args__ = (
        Index("ix_veterinary_visits_animal_id", "animal_id"),
        Index("ix_veterinary_visits_vet_id", "vet_id"),
        Index("ix_veterinary_visits_visit_date", "visit_date"),
    )

    animal_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("animals.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    vet_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    visit_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, index=True
    )
    diagnosis: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    treatment: Mapped[Optional[str]] = mapped_column(String(1024), nullable=True)
    cost: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    currency: Mapped[str] = mapped_column(String(3), default="USD")
    notes: Mapped[Optional[str]] = mapped_column(String(1024), nullable=True)

    animal: Mapped["Animal"] = relationship(
        "Animal", back_populates="veterinary_visits"
    )
    vet: Mapped["User"] = relationship("User", back_populates="veterinary_visits")

    def __repr__(self) -> str:
        return f"<VeterinaryVisit(id={self.id}, animal_id={self.animal_id})>"
