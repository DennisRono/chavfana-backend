from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from typing import List

from chavfana.controllers.farms import FarmController
from chavfana.dependencies.auth import GetCurrentUser
from chavfana.schemas.farm import FarmCreate, FarmRead, PlotCreate, PlotRead
from chavfana.db.database import get_db

farms_router = APIRouter()


@farms_router.post("/", response_model=None)
async def create_farm(
    request_data: FarmCreate,
    current_user: GetCurrentUser,
    db: AsyncSession = Depends(get_db),
):
    return await FarmController.create_farm(db, request_data)


@farms_router.get("/{farm_id}", response_model=FarmRead)
async def get_farm(
    farm_id: UUID,
    current_user: GetCurrentUser,
    db: AsyncSession = Depends(get_db),
):
    return await FarmController.get_farm_by_id(db, farm_id)


@farms_router.get("/owner/{owner_id}", response_model=List[FarmRead])
async def get_farms_by_owner(
    owner_id: UUID,
    current_user: GetCurrentUser,
    db: AsyncSession = Depends(get_db),
):
    return await FarmController.get_farms_by_owner(db, owner_id)


@farms_router.patch("/{farm_id}", response_model=FarmRead)
async def update_farm(
    farm_id: UUID,
    request_data: dict,
    current_user: GetCurrentUser,
    db: AsyncSession = Depends(get_db),
):
    return await FarmController.update_farm(db, farm_id, request_data)


@farms_router.post("/plots", response_model=None)
async def create_plot(
    request_data: PlotCreate,
    current_user: GetCurrentUser,
    db: AsyncSession = Depends(get_db),
):
    return await FarmController.create_plot(db, request_data)


@farms_router.get("/plots/{plot_id}", response_model=PlotRead)
async def get_plot(
    plot_id: UUID,
    current_user: GetCurrentUser,
    db: AsyncSession = Depends(get_db),
):
    return await FarmController.get_plot_by_id(db, plot_id)


@farms_router.get("/{farm_id}/plots", response_model=List[PlotRead])
async def get_plots_by_farm(
    farm_id: UUID,
    current_user: GetCurrentUser,
    db: AsyncSession = Depends(get_db),
):
    return await FarmController.get_plots_by_farm(db, farm_id)


@farms_router.patch("/plots/{plot_id}", response_model=PlotRead)
async def update_plot(
    plot_id: UUID,
    request_data: dict,
    current_user: GetCurrentUser,
    db: AsyncSession = Depends(get_db),
):
    return await FarmController.update_plot(db, plot_id, request_data)


@farms_router.delete("/plots/{plot_id}", status_code=204)
async def delete_plot(
    plot_id: UUID,
    current_user: GetCurrentUser,
    db: AsyncSession = Depends(get_db),
):
    await FarmController.delete_plot(db, plot_id)
