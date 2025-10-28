from __future__ import annotations

import uuid
from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, model_validator


class SoilAnalysisCreate(BaseModel):
    plot_id: uuid.UUID
    sample_date: date
    phosphorous: Optional[float] = Field(None, ge=0)
    potassium: Optional[float] = Field(None, ge=0)
    nitrogen: Optional[float] = Field(None, ge=0)
    soil_ph: Optional[float] = Field(None, ge=0, le=14)
    organic_matter: Optional[float] = Field(None, ge=0)
    notes: Optional[str] = Field(None, max_length=1024)
    lab_report_url: Optional[str] = Field(None, max_length=500)

    model_config = ConfigDict(from_attributes=True)

    @model_validator(mode="before")
    def validate_ph(cls, values):
        
        if isinstance(values, dict):
            ph = values.get("soil_ph")
            if ph is not None and (ph < 0 or ph > 14):
                raise ValueError("soil_ph must be between 0 and 14")
        return values


class SoilAnalysisRead(BaseModel):
    id: uuid.UUID
    plot_id: uuid.UUID
    sample_date: date
    phosphorous: Optional[float]
    potassium: Optional[float]
    nitrogen: Optional[float]
    soil_ph: Optional[float]
    organic_matter: Optional[float]
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class WeatherObservationCreate(BaseModel):
    farm_id: uuid.UUID
    observed_at: datetime
    temperature: Optional[float] = None
    humidity: Optional[float] = Field(None, ge=0, le=100)
    rainfall_mm: Optional[float] = Field(None, ge=0)
    wind_speed: Optional[float] = Field(None, ge=0)
    wind_direction: Optional[str] = Field(None, max_length=20)
    notes: Optional[str] = Field(None, max_length=500)

    model_config = ConfigDict(from_attributes=True)


class WeatherObservationRead(BaseModel):
    id: uuid.UUID
    farm_id: uuid.UUID
    observed_at: datetime
    temperature: Optional[float]
    humidity: Optional[float]
    rainfall_mm: Optional[float]
    wind_speed: Optional[float]
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class SeasonCreate(BaseModel):
    farm_id: uuid.UUID
    name: str = Field(..., min_length=2, max_length=200)
    start_date: date
    end_date: date
    notes: Optional[str] = Field(None, max_length=1024)

    model_config = ConfigDict(from_attributes=True)

    @model_validator(mode="before")
    def validate_dates(cls, values):
        
        if isinstance(values, dict):
            start = values.get("start_date")
            end = values.get("end_date")
            if start and end and start > end:
                raise ValueError("start_date must be <= end_date")
        return values


class SeasonRead(BaseModel):
    id: uuid.UUID
    farm_id: uuid.UUID
    name: str
    start_date: date
    end_date: date
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
