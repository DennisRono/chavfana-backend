from typing import Optional, List
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, with_polymorphic

from chavfana.models.farm import Farm
from chavfana.models.plot import Plot
from chavfana.models.project import (
    Project,
    PlantingProject,
    AnimalKeepingProject,
    PlantingEvent,
)
from chavfana.schemas.project import (
    ProjectCreate,
    PlantingProjectCreate,
    AnimalKeepingProjectCreate,
    PlantingEventCreate,
    ProjectRead,
)
from chavfana.core.exceptions import NotFoundError


class ProjectController:
    @staticmethod
    async def create_planting_project(
        db: AsyncSession, request_data: PlantingProjectCreate
    ) -> PlantingProject:
        if request_data.plot_id:
            result = await db.scalars(
                select(Plot).where(Plot.id == request_data.plot_id)
            )
            plot = result.scalar_one_or_none()
            farm_id = plot.farm_id if plot else None

        project = PlantingProject(
            farm_id=request_data.farm_id or farm_id,
            plot_id=request_data.plot_id or None,
            owner_id=request_data.owner_id,
            name=request_data.name,
            project_type="PlantingProject",
            status=request_data.status,
            start_date=request_data.start_date,
            end_date=request_data.end_date,
            notes=request_data.notes,
            species_id=request_data.species_id,
            expected_yield=request_data.expected_yield,
            yield_unit=request_data.yield_unit,
            expected_revenue=request_data.expected_revenue,
            irrigation_type=request_data.irrigation_type,
            soil_analysis_id=request_data.soil_analysis_id,
        )
        db.add(project)
        await db.flush()
        return project

    @staticmethod
    async def create_animal_keeping_project(
        db: AsyncSession, request_data: AnimalKeepingProjectCreate
    ) -> AnimalKeepingProject:
        project = AnimalKeepingProject(
            farm_id=request_data.farm_id,
            owner_id=request_data.owner_id,
            name=request_data.name,
            project_type="AnimalKeepingProject",
            status=request_data.status,
            start_date=request_data.start_date,
            end_date=request_data.end_date,
            notes=request_data.notes,
            housing_type=request_data.housing_type,
            pasture_info=request_data.pasture_info,
            carrying_capacity=request_data.carrying_capacity,
        )
        db.add(project)
        await db.flush()
        return project

    @staticmethod
    async def get_all_projects(db: AsyncSession):
        project_with_subclasses = with_polymorphic(
            Project, [PlantingProject, AnimalKeepingProject]
        )

        stmt = (
            select(project_with_subclasses)
            .options(
                selectinload(project_with_subclasses.owner),
                selectinload(project_with_subclasses.farm).selectinload(Farm.plots),
            )
            .where(project_with_subclasses.is_deleted == False)
        )

        result = await db.execute(stmt)
        projects = result.scalars().unique().all()
        return projects

    @staticmethod
    async def get_project_by_id(
        db: AsyncSession, project_id: UUID
    ) -> Optional[Project]:
        stmt = select(Project).where(Project.id == project_id)
        result = await db.execute(stmt)
        return result.scalar_one_or_none()

    @staticmethod
    async def get_projects_by_farm(db: AsyncSession, farm_id: UUID) -> List[Project]:
        stmt = select(Project).where(Project.farm_id == farm_id)
        result = await db.execute(stmt)
        return result.scalars().all()

    @staticmethod
    async def create_planting_event(
        db: AsyncSession, request_data: PlantingEventCreate
    ) -> PlantingEvent:
        event = PlantingEvent(
            project_id=request_data.project_id,
            plot_id=request_data.plot_id,
            planting_date=request_data.planting_date,
            end_date=request_data.end_date,
            area_size=request_data.area_size,
            area_unit=request_data.area_unit,
            stage=request_data.stage,
            notes=request_data.notes,
            species_details=request_data.species_details,
        )
        db.add(event)
        await db.flush()
        return event

    @staticmethod
    async def get_planting_events_by_project(
        db: AsyncSession, project_id: UUID
    ) -> List[PlantingEvent]:
        stmt = select(PlantingEvent).where(PlantingEvent.project_id == project_id)
        result = await db.execute(stmt)
        return result.scalars().all()
