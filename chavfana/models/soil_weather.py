from __future__ import annotations

import uuid
from datetime import date, datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy import Index, String, Float, Date, DateTime, JSON, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from chavfana.models.base import BaseModel

if TYPE_CHECKING:
    from chavfana.models.farm import Farm, Plot


class SoilAnalysis(BaseModel):

    __tablename__ = "soil_analyses"
    __table_args__ = (
        Index("ix_soil_analyses_plot_id", "plot_id"),
        Index("ix_soil_analyses_sample_date", "sample_date"),
    )

    plot_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("plots.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    sample_date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    phosphorous: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    potassium: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    nitrogen: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    soil_ph: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    organic_matter: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    notes: Mapped[Optional[str]] = mapped_column(String(1024), nullable=True)
    lab_report_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)

    def __repr__(self) -> str:
        return f"<SoilAnalysis(id={self.id}, plot_id={self.plot_id})>"


class WeatherObservation(BaseModel):
    __tablename__ = "weather_observations"
    __table_args__ = (
        Index("ix_weather_observations_farm_id", "farm_id"),
        Index("ix_weather_observations_observed_at", "observed_at"),
    )

    farm_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("farms.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    observed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, index=True
    )
    temperature: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    humidity: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    rainfall_mm: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    wind_speed: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    wind_direction: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    notes: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)

    def __repr__(self) -> str:
        return f"<WeatherObservation(id={self.id}, farm_id={self.farm_id})>"


class Season(BaseModel):
    __tablename__ = "seasons"
    __table_args__ = (Index("ix_seasons_farm_id", "farm_id"),)

    farm_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("farms.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[date] = mapped_column(Date, nullable=False)
    notes: Mapped[Optional[str]] = mapped_column(String(1024), nullable=True)

    def __repr__(self) -> str:
        return f"<Season(id={self.id}, name={self.name}, farm_id={self.farm_id})>"
