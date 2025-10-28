from __future__ import annotations

import uuid
from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, model_validator


class InventoryItemCreate(BaseModel):
    farm_id: uuid.UUID
    name: str = Field(..., min_length=2, max_length=200)
    sku: str = Field(..., min_length=1, max_length=100)
    quantity: float = Field(..., ge=0)
    unit: str = Field(..., max_length=20)
    unit_cost: float = Field(..., gt=0)
    currency: str = Field(default="USD", max_length=3)
    supplier_id: Optional[uuid.UUID] = None
    reorder_level: float = Field(default=0.0, ge=0)

    model_config = ConfigDict(from_attributes=True)


class InventoryItemUpdate(BaseModel):
    quantity: Optional[float] = Field(None, ge=0)
    unit_cost: Optional[float] = Field(None, gt=0)
    reorder_level: Optional[float] = Field(None, ge=0)

    model_config = ConfigDict(from_attributes=True)


class InventoryItemRead(BaseModel):
    id: uuid.UUID
    farm_id: uuid.UUID
    name: str
    sku: str
    quantity: float
    unit: str
    unit_cost: float
    currency: str
    reorder_level: float
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class TransactionCreate(BaseModel):
    farm_id: uuid.UUID
    project_id: Optional[uuid.UUID] = None
    item_id: Optional[uuid.UUID] = None
    transaction_type: str = Field(..., max_length=50)
    amount: float = Field(..., ne=0)
    currency: str = Field(default="USD", max_length=3)
    quantity: Optional[float] = Field(None, gt=0)
    date: date
    notes: Optional[str] = Field(None, max_length=1024)
    related_party_id: Optional[uuid.UUID] = None
    created_by_id: Optional[uuid.UUID] = None

    model_config = ConfigDict(from_attributes=True)

    @model_validator(mode="before")
    def validate_amount(cls, values):

        if isinstance(values, dict):
            tx_type = values.get("transaction_type", "").upper()
            amount = values.get("amount")
            if tx_type in ("INCOME", "SALE") and amount and amount < 0:
                raise ValueError(f"{tx_type} amount must be positive")
            if tx_type in ("EXPENSE", "PURCHASE") and amount and amount > 0:
                values["amount"] = -abs(amount)
        return values


class TransactionRead(BaseModel):
    id: uuid.UUID
    farm_id: uuid.UUID
    transaction_type: str
    amount: float
    currency: str
    date: date
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
