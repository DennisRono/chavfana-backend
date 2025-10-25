from typing import Optional, List
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from chavfana.models.animal import Animal, AnimalGroup
from chavfana.core.exceptions import NotFoundError


class AnimalController:
    @staticmethod
    async def get_animal_by_id(db: AsyncSession, animal_id: UUID) -> Optional[Animal]:
        stmt = select(Animal).where(Animal.id == animal_id)
        result = await db.execute(stmt)
        return result.scalar_one_or_none()

    @staticmethod
    async def get_animals_by_project(db: AsyncSession, project_id: UUID) -> List[Animal]:
        stmt = select(Animal).where(Animal.project_id == project_id)
        result = await db.execute(stmt)
        return result.scalars().all()

    @staticmethod
    async def get_animal_group_by_id(db: AsyncSession, group_id: UUID) -> Optional[AnimalGroup]:
        stmt = select(AnimalGroup).where(AnimalGroup.id == group_id)
        result = await db.execute(stmt)
        return result.scalar_one_or_none()

    @staticmethod
    async def get_animal_groups_by_project(
        db: AsyncSession, project_id: UUID
    ) -> List[AnimalGroup]:
        stmt = select(AnimalGroup).where(AnimalGroup.project_id == project_id)
        result = await db.execute(stmt)
        return result.scalars().all()
