from typing import Optional, List
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from chavfana.models.farm import Farm
from chavfana.schemas.farm import FarmCreate
from chavfana.core.exceptions import NotFoundError


class FarmController:
    @staticmethod
    async def create_farm(db: AsyncSession, request_data: FarmCreate) -> Farm:
        farm = Farm(
            owner_id=request_data.owner_id,
            name=request_data.name,
            description=request_data.description,
            country=request_data.country,
            city=request_data.city,
            address=request_data.address,
            geo_coordinate=request_data.geo_coordinate,
            rectangle_boundary=request_data.rectangle_boundary,
            area_size=request_data.area_size,
            area_unit=request_data.area_unit,
            time_zone=request_data.time_zone,
        )
        db.add(farm)
        await db.flush()
        return farm

    @staticmethod
    async def get_farm_by_id(db: AsyncSession, farm_id: UUID) -> Optional[Farm]:
        stmt = select(Farm).where(Farm.id == farm_id)
        result = await db.execute(stmt)
        return result.scalar_one_or_none()

    @staticmethod
    async def get_farms_by_owner(db: AsyncSession, owner_id: UUID) -> List[Farm]:
        stmt = select(Farm).where(Farm.owner_id == owner_id)
        result = await db.execute(stmt)
        return result.scalars().all()

    @staticmethod
    async def update_farm(db: AsyncSession, farm_id: UUID, request_data: dict) -> Optional[Farm]:
        farm = await FarmController.get_farm_by_id(db, farm_id)
        if not farm:
            raise NotFoundError(f"Farm with id {farm_id} not found")
        for key, value in request_data.items():
            if value is not None:
                setattr(farm, key, value)
        await db.flush()
        return farm
