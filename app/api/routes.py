from fastapi import APIRouter
from app.api.endpoints.auth import auth_router
from app.api.endpoints.animals import animals_router
from app.api.endpoints.farms import farms_router
from app.api.endpoints.projects import projects_router

api_router = APIRouter()

api_router.include_router(auth_router, prefix="/auth", tags=["Auth"])
api_router.include_router(animals_router, prefix="/animals", tags=["Animals"])
api_router.include_router(farms_router, prefix="/farms", tags=["Farms"])
api_router.include_router(projects_router, prefix="/projects", tags=["Projects"])
