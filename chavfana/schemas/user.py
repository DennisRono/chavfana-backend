from __future__ import annotations

import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, model_validator


class UserCreate(BaseModel):
    email: str = Field(..., min_length=5, max_length=255)
    full_name: str = Field(..., min_length=2, max_length=255)
    phone: Optional[str] = Field(None, max_length=20)
    role: str = Field(default="FARMER", max_length=50)
    password: str = Field(..., min_length=8)
    profile_data: Optional[dict] = None

    model_config = ConfigDict(from_attributes=True)

    @model_validator(mode="before")
    def normalize_email(cls, values):
        
        if isinstance(values, dict) and "email" in values:
            values["email"] = values["email"].strip().lower()
        return values


class UserUpdate(BaseModel):
    email: Optional[str] = Field(None, min_length=5, max_length=255)
    full_name: Optional[str] = Field(None, min_length=2, max_length=255)
    phone: Optional[str] = Field(None, max_length=20)
    role: Optional[str] = Field(None, max_length=50)
    is_active: Optional[bool] = None
    profile_data: Optional[dict] = None

    model_config = ConfigDict(from_attributes=True)

    @model_validator(mode="before")
    def normalize_email(cls, values):
        
        if isinstance(values, dict) and "email" in values and values["email"]:
            values["email"] = values["email"].strip().lower()
        return values


class UserRead(BaseModel):
    id: uuid.UUID
    email: str
    full_name: str
    phone: Optional[str]
    role: str
    is_active: bool
    last_login: Optional[datetime]
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class EmployeeCreate(BaseModel):
    user_id: uuid.UUID
    farm_id: uuid.UUID
    position: str = Field(..., min_length=2, max_length=100)
    employment_start: datetime
    employment_end: Optional[datetime] = None
    salary_amount: Optional[float] = Field(None, gt=0)
    salary_currency: str = Field(default="USD", max_length=3)

    model_config = ConfigDict(from_attributes=True)


class EmployeeRead(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    farm_id: uuid.UUID
    position: str
    employment_start: datetime
    employment_end: Optional[datetime]
    salary_amount: Optional[float]
    salary_currency: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

