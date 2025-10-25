from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from chavfana.controllers.farms import FarmController
from chavfana.schemas.farm import FarmCreate, FarmRead
from chavfana.db.database import get_db

farms_router = APIRouter()

@farms_router.post("/", response_model=FarmRead)
async def create_farm(
    request_data: FarmCreate,
    db: AsyncSession = Depends(get_db),
):
    try:
        farm = await FarmController.create_farm(db, request_data)
        await db.commit()
        await db.refresh(farm)
        return farm
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@farms_router.get("/{farm_id}", response_model=FarmRead)
async def get_farm(
    farm_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    farm = await FarmController.get_farm_by_id(db, farm_id)
    if not farm:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Farm not found")
    return farm

@farms_router.get("/owner/{owner_id}")
async def get_farms_by_owner(
    owner_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    farms = await FarmController.get_farms_by_owner(db, owner_id)
    return farms
