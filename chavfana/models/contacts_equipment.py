from __future__ import annotations

import uuid
from datetime import date
from typing import Optional

from sqlalchemy import Index, String, Float, Date

from chavfana.models.base import BaseModel
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID


class Contact(BaseModel):
    __tablename__ = "contacts"
    __table_args__ = (
        Index("ix_contacts_contact_type", "contact_type"),
        Index("ix_contacts_email", "email"),
    )

    contact_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        comment="SUPPLIER, BUYER, SERVICE_PROVIDER, VET, AGRONOMIST",
    )
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    phone: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    email: Mapped[Optional[str]] = mapped_column(String(255), nullable=True, index=True)
    address: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    notes: Mapped[Optional[str]] = mapped_column(String(1024), nullable=True)

    def __repr__(self) -> str:
        return f"<Contact(id={self.id}, name={self.name}, type={self.contact_type})>"


class Equipment(BaseModel):
    __tablename__ = "equipment"
    __table_args__ = (
        Index("ix_equipment_farm_id", "farm_id"),
        Index("ix_equipment_status", "status"),
    )

    farm_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), nullable=False, index=True
    )
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    serial_no: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    purchase_date: Mapped[date] = mapped_column(Date, nullable=False)
    purchase_cost: Mapped[float] = mapped_column(Float, nullable=False)
    currency: Mapped[str] = mapped_column(String(3), default="USD")
    last_service_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    status: Mapped[str] = mapped_column(
        String(50), default="Active", comment="Active, Maintenance, Retired"
    )

    def __repr__(self) -> str:
        return f"<Equipment(id={self.id}, name={self.name}, farm_id={self.farm_id})>"
