from __future__ import annotations

import uuid
from datetime import date
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, model_validator


class AnimalGroupCreate(BaseModel):
    project_id: uuid.UUID
    group_name: str = Field(..., min_length=2, max_length=200)
    housing: str = Field(..., max_length=100)
    starting_number: int = Field(..., gt=0)
    average_weight: Optional[float] = Field(None, gt=0)
    average_age: Optional[float] = Field(None, gt=0)
    quarantine_info: Optional[str] = Field(None, max_length=500)
    notes: Optional[str] = Field(None, max_length=1024)

    model_config = ConfigDict(from_attributes=True)



class AnimalGroupRead(BaseModel):
    id: uuid.UUID
    project_id: uuid.UUID
    group_name: str
    housing: str
    starting_number: int
    average_weight: Optional[float]
    disease_alerts: bool
    created_at: str

    model_config = ConfigDict(from_attributes=True)


class AnimalCreate(BaseModel):
    project_id: uuid.UUID
    group_id: Optional[uuid.UUID] = None
    tag: str = Field(..., min_length=1, max_length=100)
    breed: Optional[str] = Field(None, max_length=100)
    name: Optional[str] = Field(None, max_length=100)
    arrival_date: date
    birthday: Optional[date] = None
    animal_type: str = Field(..., max_length=50)
    gender: str = Field(..., max_length=20)
    weight: Optional[float] = Field(None, gt=0)
    age_estimate: Optional[float] = Field(None, gt=0)
    health_status: str = Field(default="Healthy", max_length=50)
    insurance_policy: Optional[dict] = None

    model_config = ConfigDict(from_attributes=True)

    @model_validator(mode="before")
    def validate_dates(cls, values):
        if isinstance(values, dict):
            birthday = values.get("birthday")
            arrival = values.get("arrival_date")
            if birthday and arrival and birthday > arrival:
                raise ValueError("birthday must be <= arrival_date")
        return values


class AnimalUpdate(BaseModel):
    breed: Optional[str] = Field(None, max_length=100)
    name: Optional[str] = Field(None, max_length=100)
    weight: Optional[float] = Field(None, gt=0)
    health_status: Optional[str] = Field(None, max_length=50)
    is_active: Optional[bool] = None

    model_config = ConfigDict(from_attributes=True)


class AnimalRead(BaseModel):
    id: uuid.UUID
    project_id: uuid.UUID
    tag: str
    breed: Optional[str]
    name: Optional[str]
    animal_type: str
    gender: str
    health_status: str
    is_active: bool
    created_at: str

    model_config = ConfigDict(from_attributes=True)
