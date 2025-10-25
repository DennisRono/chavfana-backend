from __future__ import annotations

import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy import Index, String, Integer, DateTime, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from chavfana.models.base import BaseModel


class Attachment(BaseModel):
    __tablename__ = "attachments"
    __table_args__ = (
        Index("ix_attachments_owner_type_id", "owner_type", "owner_id"),
        Index("ix_attachments_uploaded_by_id", "uploaded_by_id"),
    )

    owner_type: Mapped[str] = mapped_column(
        String(100), nullable=False, comment="Project, Plot, SoilAnalysis, etc."
    )
    owner_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), nullable=False, index=True
    )
    file_path: Mapped[str] = mapped_column(String(500), nullable=False)
    mime_type: Mapped[str] = mapped_column(String(100), nullable=False)
    size_bytes: Mapped[int] = mapped_column(Integer, nullable=False)
    uploaded_by_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), nullable=False, index=True
    )
    uploaded_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )

    def __repr__(self) -> str:
        return f"<Attachment(id={self.id}, owner_type={self.owner_type})>"


class AuditLog(BaseModel):
    __tablename__ = "audit_logs"
    __table_args__ = (
        Index("ix_audit_logs_entity_type_id", "entity_type", "entity_id"),
        Index("ix_audit_logs_changed_by_id", "changed_by_id"),
        Index("ix_audit_logs_changed_at", "changed_at"),
    )

    entity_type: Mapped[str] = mapped_column(String(100), nullable=False)
    entity_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), nullable=False, index=True
    )
    change_type: Mapped[str] = mapped_column(
        String(50), nullable=False, comment="CREATE, UPDATE, DELETE"
    )
    changed_by_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), nullable=False, index=True
    )
    changed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, index=True
    )
    diff: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)

    def __repr__(self) -> str:
        return f"<AuditLog(id={self.id}, entity_type={self.entity_type})>"
