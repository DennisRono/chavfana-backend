from typing import Optional, List
from uuid import UUID

from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

from chavfana.models.farm import Farm
from chavfana.models.plot import Plot
from chavfana.schemas.farm import FarmCreate, PlotCreate
from chavfana.core.exceptions import (
    NotFoundError,
    DatabaseError,
    DatabaseIntegrityError,
    BusinessLogicError,
)


class FarmController:
    @staticmethod
    async def create_farm(db: AsyncSession, request_data: FarmCreate) -> Farm:
        try:
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
            await db.commit()
            await db.refresh(farm)
            return farm
        except SQLAlchemyError as e:
            await db.rollback()
            raise DatabaseError(message=str(e))

    @staticmethod
    async def get_farm_by_id(db: AsyncSession, farm_id: UUID) -> Optional[Farm]:
        stmt = select(Farm).where(Farm.id == farm_id)
        result = await db.execute(stmt)
        farm = result.scalar_one_or_none()
        if not farm:
            raise NotFoundError(resource_type="Farm", resource_id=str(farm_id))
        return farm

    @staticmethod
    async def get_farms_by_owner(db: AsyncSession, owner_id: UUID) -> List[Farm]:
        stmt = select(Farm).where(Farm.owner_id == owner_id)
        result = await db.execute(stmt)
        return result.scalars().all()

    @staticmethod
    async def update_farm(db: AsyncSession, farm_id: UUID, request_data: dict) -> Farm:
        farm = await FarmController.get_farm_by_id(db, farm_id)
        try:
            for key, value in request_data.items():
                if value is not None:
                    setattr(farm, key, value)
            await db.flush()
            await db.commit()
            await db.refresh(farm)
            return farm
        except SQLAlchemyError as e:
            await db.rollback()
            raise DatabaseError(message=str(e))

    @staticmethod
    async def create_plot(db: AsyncSession, request_data: PlotCreate) -> Plot:
        try:
            farm = await FarmController.get_farm_by_id(db, request_data.farm_id)

            plot = Plot(
                farm_id=farm.id,
                name=request_data.name,
                plot_code=request_data.plot_code,
                area_size=request_data.area_size,
                area_unit=request_data.area_unit,
                soil_profile=request_data.soil_profile,
                gps_bounds=request_data.gps_bounds,
                current_crop_id=request_data.current_crop_id,
            )

            db.add(plot)
            await db.flush()
            await db.commit()
            await db.refresh(plot)
            return plot
        except SQLAlchemyError as e:
            await db.rollback()
            raise DatabaseError(message=str(e))

    @staticmethod
    async def get_plot_by_id(db: AsyncSession, plot_id: UUID) -> Plot:
        stmt = select(Plot).where(Plot.id == plot_id)
        result = await db.execute(stmt)
        plot = result.scalar_one_or_none()
        if not plot:
            raise NotFoundError(resource_type="Plot", resource_id=str(plot_id))
        return plot

    @staticmethod
    async def get_plots_by_farm(db: AsyncSession, farm_id: UUID) -> List[Plot]:
        stmt = select(Plot).where(Plot.farm_id == farm_id)
        result = await db.execute(stmt)
        return result.scalars().all()

    @staticmethod
    async def update_plot(db: AsyncSession, plot_id: UUID, request_data: dict) -> Plot:
        plot = await FarmController.get_plot_by_id(db, plot_id)
        try:
            for key, value in request_data.items():
                if value is not None:
                    setattr(plot, key, value)
            await db.flush()
            await db.commit()
            await db.refresh(plot)
            return plot
        except SQLAlchemyError as e:
            await db.rollback()
            raise DatabaseError(message=str(e))

    @staticmethod
    async def delete_plot(db: AsyncSession, plot_id: UUID) -> None:
        plot = await FarmController.get_plot_by_id(db, plot_id)
        try:
            await db.delete(plot)
            await db.commit()
        except SQLAlchemyError as e:
            await db.rollback()
            raise DatabaseError(message=str(e))
