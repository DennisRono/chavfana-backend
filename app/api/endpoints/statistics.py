from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from chavfana.controllers.statistics import StatisticsController
from chavfana.db.database import get_db
from chavfana.dependencies.auth import GetCurrentUser

statistics_router = APIRouter()


@statistics_router.get("/", summary="Get system-wide farm statistics")
async def get_statistics(
    current_user: GetCurrentUser,
    db: AsyncSession = Depends(get_db),
):
    try:
        return await StatisticsController.get_all_statistics(db)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
