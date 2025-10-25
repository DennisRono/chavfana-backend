from __future__ import annotations

import uuid
from datetime import date
from typing import TYPE_CHECKING, Optional

from sqlalchemy import Index, String, Float, Date, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from chavfana.models.base import BaseModel

if TYPE_CHECKING:
    from chavfana.models.farm import Farm
    from chavfana.models.project import Project


class InventoryItem(BaseModel):
    __tablename__ = "inventory_items"
    __table_args__ = (
        Index("ix_inventory_items_farm_id", "farm_id"),
        Index("ix_inventory_items_sku", "sku", unique=True),
    )

    farm_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("farms.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    sku: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    quantity: Mapped[float] = mapped_column(Float, nullable=False)
    unit: Mapped[str] = mapped_column(
        String(20), nullable=False, comment="KG, LITER, UNIT, POUND"
    )
    unit_cost: Mapped[float] = mapped_column(Float, nullable=False)
    currency: Mapped[str] = mapped_column(String(3), default="USD")
    supplier_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), nullable=True
    )
    reorder_level: Mapped[float] = mapped_column(Float, default=0.0)

    def __repr__(self) -> str:
        return f"<InventoryItem(id={self.id}, sku={self.sku}, quantity={self.quantity})>"


class Transaction(BaseModel):
    __tablename__ = "transactions"
    __table_args__ = (
        Index("ix_transactions_farm_id", "farm_id"),
        Index("ix_transactions_project_id", "project_id"),
        Index("ix_transactions_date", "date"),
        Index("ix_transactions_farm_date", "farm_id", "date"),
    )

    farm_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("farms.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    project_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("projects.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    item_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("inventory_items.id", ondelete="SET NULL"),
        nullable=True,
    )
    transaction_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        comment="PURCHASE, SALE, EXPENSE, INCOME",
    )
    amount: Mapped[float] = mapped_column(Float, nullable=False)
    currency: Mapped[str] = mapped_column(String(3), default="USD")
    quantity: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    notes: Mapped[Optional[str]] = mapped_column(String(1024), nullable=True)
    related_party_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), nullable=True
    )
    created_by_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), nullable=True
    )

    def __repr__(self) -> str:
        return f"<Transaction(id={self.id}, type={self.transaction_type}, amount={self.amount})>"
