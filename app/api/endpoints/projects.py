from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from chavfana.controllers.projects import ProjectController
from chavfana.dependencies.auth import GetCurrentUser
from chavfana.schemas.project import (
    PlantingProjectCreate,
    PlantingProjectRead,
    AnimalKeepingProjectCreate,
    AnimalKeepingProjectRead,
    PlantingEventCreate,
    PlantingEventRead,
)
from chavfana.db.database import get_db

projects_router = APIRouter()

@projects_router.post("/planting", response_model=PlantingProjectRead)
async def create_planting_project(
    request_data: PlantingProjectCreate,
    current_user: GetCurrentUser,
    db: AsyncSession = Depends(get_db),
):
    try:
        project = await ProjectController.create_planting_project(db, request_data)
        await db.commit()
        await db.refresh(project)
        return project
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@projects_router.post("/animal-keeping", response_model=AnimalKeepingProjectRead)
async def create_animal_keeping_project(
    request_data: AnimalKeepingProjectCreate,
    current_user: GetCurrentUser,
    db: AsyncSession = Depends(get_db),
):
    try:
        project = await ProjectController.create_animal_keeping_project(db, request_data)
        await db.commit()
        await db.refresh(project)
        return project
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@projects_router.get("/{project_id}", response_model=PlantingProjectRead)
async def get_project(
    project_id: UUID,
    current_user: GetCurrentUser,
    db: AsyncSession = Depends(get_db),
):
    project = await ProjectController.get_project_by_id(db, project_id)
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    return project

@projects_router.get("/farm/{farm_id}")
async def get_projects_by_farm(
    farm_id: UUID,
    current_user: GetCurrentUser,
    db: AsyncSession = Depends(get_db),
):
    projects = await ProjectController.get_projects_by_farm(db, farm_id)
    return projects

@projects_router.post("/planting-events", response_model=PlantingEventRead)
async def create_planting_event(
    request_data: PlantingEventCreate,
    current_user: GetCurrentUser,
    db: AsyncSession = Depends(get_db),
):
    try:
        event = await ProjectController.create_planting_event(db, request_data)
        await db.commit()
        await db.refresh(event)
        return event
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@projects_router.get("/planting-events/{project_id}")
async def get_planting_events(
    project_id: UUID,
    current_user: GetCurrentUser,
    db: AsyncSession = Depends(get_db),
):
    events = await ProjectController.get_planting_events_by_project(db, project_id)
    return events
