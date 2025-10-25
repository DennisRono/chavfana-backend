from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from chavfana.controllers.animals import AnimalController
from chavfana.db.database import get_db
from chavfana.dependencies.auth import GetCurrentUser

animals_router = APIRouter()

@animals_router.get("/{animal_id}")
async def get_animal(
    animal_id: UUID,
    current_user: GetCurrentUser,
    db: AsyncSession = Depends(get_db),
):
    animal = await AnimalController.get_animal_by_id(db, animal_id)
    if not animal:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Animal not found")
    return animal

@animals_router.get("/project/{project_id}")
async def get_animals_by_project(
    project_id: UUID,
    current_user: GetCurrentUser,
    db: AsyncSession = Depends(get_db),
):
    animals = await AnimalController.get_animals_by_project(db, project_id)
    return animals

@animals_router.get("/groups/{project_id}")
async def get_animal_groups(
    project_id: UUID,
    current_user: GetCurrentUser,
    db: AsyncSession = Depends(get_db),
):
    groups = await AnimalController.get_animal_groups_by_project(db, project_id)
    return groups
