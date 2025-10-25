from __future__ import annotations

import uuid
from datetime import date
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, model_validator


class ProjectCreate(BaseModel):
    farm_id: uuid.UUID
    owner_id: uuid.UUID
    name: str = Field(..., min_length=2, max_length=200)
    status: str = Field(default="Planning", max_length=50)
    start_date: date
    end_date: Optional[date] = None
    notes: Optional[str] = Field(None, max_length=2048)

    model_config = ConfigDict(from_attributes=True)

    @model_validator(mode="before")
    def validate_dates(cls, values):
        
        if isinstance(values, dict):
            start = values.get("start_date")
            end = values.get("end_date")
            if start and end and start > end:
                raise ValueError("start_date must be <= end_date")
        return values


class PlantingProjectCreate(ProjectCreate):
    project_type: str = Field(default="PlantingProject")
    species_id: Optional[uuid.UUID] = None
    expected_yield: Optional[float] = Field(None, gt=0)
    yield_unit: Optional[str] = Field(None, max_length=50)
    expected_revenue: Optional[float] = Field(None, gt=0)
    irrigation_type: Optional[str] = Field(None, max_length=100)
    soil_analysis_id: Optional[uuid.UUID] = None


class PlantingProjectRead(BaseModel):
    id: uuid.UUID
    farm_id: uuid.UUID
    owner_id: uuid.UUID
    name: str
    status: str
    start_date: date
    end_date: Optional[date]
    expected_yield: Optional[float]
    yield_unit: Optional[str]
    expected_revenue: Optional[float]
    created_at: str

    model_config = ConfigDict(from_attributes=True)


class PlantingEventCreate(BaseModel):
    project_id: uuid.UUID
    plot_id: uuid.UUID
    planting_date: date
    end_date: Optional[date] = None
    area_size: float = Field(..., gt=0)
    area_unit: str = Field(default="HECTARE", max_length=20)
    stage: str = Field(default="Seedling", max_length=50)
    notes: Optional[str] = Field(None, max_length=1024)
    species_details: Optional[dict] = None

    model_config = ConfigDict(from_attributes=True)

    @model_validator(mode="before")
    def validate_dates(cls, values):
        
        if isinstance(values, dict):
            start = values.get("planting_date")
            end = values.get("end_date")
            if start and end and start > end:
                raise ValueError("planting_date must be <= end_date")
        return values


class PlantingEventRead(BaseModel):
    id: uuid.UUID
    project_id: uuid.UUID
    plot_id: uuid.UUID
    planting_date: date
    end_date: Optional[date]
    area_size: float
    stage: str
    created_at: str

    model_config = ConfigDict(from_attributes=True)


class AnimalKeepingProjectCreate(ProjectCreate):
    project_type: str = Field(default="AnimalKeepingProject")
    housing_type: Optional[str] = Field(None, max_length=100)
    pasture_info: Optional[str] = Field(None, max_length=500)
    carrying_capacity: Optional[int] = Field(None, gt=0)


class AnimalKeepingProjectRead(BaseModel):
    id: uuid.UUID
    farm_id: uuid.UUID
    owner_id: uuid.UUID
    name: str
    status: str
    housing_type: Optional[str]
    carrying_capacity: Optional[int]
    created_at: str

    model_config = ConfigDict(from_attributes=True)
