from __future__ import annotations

from datetime import datetime
import uuid
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, model_validator


class FarmCreate(BaseModel):
    owner_id: uuid.UUID
    name: str = Field(..., min_length=2, max_length=200)
    description: Optional[str] = Field(None, max_length=1024)
    country: str = Field(..., min_length=2, max_length=2)
    city: Optional[str] = Field(None, max_length=100)
    address: Optional[str] = Field(None, max_length=255)
    geo_coordinate: Optional[dict] = None
    rectangle_boundary: Optional[dict] = None
    area_size: float = Field(..., gt=0)
    area_unit: str = Field(default="HECTARE", max_length=20)
    time_zone: str = Field(default="UTC", max_length=50)

    model_config = ConfigDict(from_attributes=True)


class FarmUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=200)
    description: Optional[str] = Field(None, max_length=1024)
    city: Optional[str] = Field(None, max_length=100)
    address: Optional[str] = Field(None, max_length=255)
    geo_coordinate: Optional[dict] = None
    rectangle_boundary: Optional[dict] = None
    area_size: Optional[float] = Field(None, gt=0)
    area_unit: Optional[str] = Field(None, max_length=20)
    time_zone: Optional[str] = Field(None, max_length=50)

    model_config = ConfigDict(from_attributes=True)


class FarmRead(BaseModel):
    id: uuid.UUID
    owner_id: uuid.UUID
    name: str
    description: Optional[str]
    country: str
    city: Optional[str]
    address: Optional[str]
    area_size: float
    area_unit: str
    time_zone: str
    created_at: str

    model_config = ConfigDict(from_attributes=True)


class PlotCreate(BaseModel):
    farm_id: uuid.UUID
    name: str = Field(..., min_length=2, max_length=200)
    plot_code: str = Field(..., min_length=1, max_length=50)
    area_size: float = Field(..., gt=0)
    area_unit: str = Field(default="HECTARE", max_length=20)
    soil_profile: Optional[dict] = None
    gps_bounds: Optional[dict] = None
    current_crop_id: Optional[uuid.UUID] = None

    model_config = ConfigDict(from_attributes=True)

    @model_validator(mode="before")
    def validate_plot_code(cls, values):
        
        if isinstance(values, dict) and "plot_code" in values:
            values["plot_code"] = values["plot_code"].strip().upper()
        return values


class PlotUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=200)
    area_size: Optional[float] = Field(None, gt=0)
    area_unit: Optional[str] = Field(None, max_length=20)
    soil_profile: Optional[dict] = None
    gps_bounds: Optional[dict] = None
    current_crop_id: Optional[uuid.UUID] = None

    model_config = ConfigDict(from_attributes=True)


class PlotRead(BaseModel):
    id: uuid.UUID
    farm_id: uuid.UUID
    name: str
    plot_code: str
    area_size: float
    area_unit: str
    current_crop_id: Optional[uuid.UUID]
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
