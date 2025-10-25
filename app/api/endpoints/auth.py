from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Dict, Any
from uuid import UUID

from chavfana.controllers.auth import AuthController
from chavfana.db.database import get_db
from chavfana.schemas.user import (
    UserCreate,
    UserRead,
    UserUpdate,
    EmployeeCreate,
    EmployeeRead,
)
from chavfana.core.exceptions import (
    NotFoundError,
    BusinessLogicError,
    AuthenticationError,
)

auth_router = APIRouter()

auth_controller = AuthController()


@auth_router.post(
    "/register", response_model=UserRead, status_code=status.HTTP_201_CREATED
)
async def register_user(request_data: UserCreate, db: AsyncSession = Depends(get_db)):
    return await auth_controller.create_user(db=db, request_data=request_data)


@auth_router.post("/login", status_code=status.HTTP_200_OK)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)
):
    return await auth_controller.login(
        db=db, email=form_data.username, password=form_data.password
    )


@auth_router.get("/users/{user_id}", response_model=UserRead)
async def get_user(user_id: UUID, db: AsyncSession = Depends(get_db)):
    return await auth_controller.get_user_by_id(db=db, user_id=user_id)


@auth_router.get("/users/email/{email}", response_model=UserRead)
async def get_user_by_email(email: str, db: AsyncSession = Depends(get_db)):
    return await auth_controller.get_user_by_email(db=db, email=email)


@auth_router.get("/users", response_model=List[UserRead])
async def get_all_users(
    skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)
):
    return await auth_controller.get_all_users(db=db, skip=skip, limit=limit)


@auth_router.get("/users/role/{role}", response_model=List[UserRead])
async def get_users_by_role(
    role: str, skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)
):
    return await auth_controller.get_users_by_role(
        db=db, role=role, skip=skip, limit=limit
    )


@auth_router.put("/users/{user_id}", response_model=UserRead)
async def update_user(
    user_id: UUID, request_data: UserUpdate, db: AsyncSession = Depends(get_db)
):
    return await auth_controller.update_user(
        db=db, user_id=user_id, request_data=request_data
    )


@auth_router.post("/users/{user_id}/deactivate", response_model=UserRead)
async def deactivate_user(user_id: UUID, db: AsyncSession = Depends(get_db)):
    return await auth_controller.deactivate_user(db=db, user_id=user_id)


@auth_router.post("/users/{user_id}/activate", response_model=UserRead)
async def activate_user(user_id: UUID, db: AsyncSession = Depends(get_db)):
    return await auth_controller.activate_user(db=db, user_id=user_id)


@auth_router.post("/users/{user_id}/change-password", status_code=status.HTTP_200_OK)
async def change_password(
    user_id: UUID,
    old_password: str,
    new_password: str,
    db: AsyncSession = Depends(get_db),
):
    return await auth_controller.change_password(
        db=db, user_id=user_id, old_password=old_password, new_password=new_password
    )


@auth_router.post(
    "/employees", response_model=EmployeeRead, status_code=status.HTTP_201_CREATED
)
async def create_employee(
    request_data: EmployeeCreate, db: AsyncSession = Depends(get_db)
):
    return await auth_controller.create_employee(db=db, request_data=request_data)


@auth_router.get("/employees/{employee_id}", response_model=EmployeeRead)
async def get_employee(employee_id: UUID, db: AsyncSession = Depends(get_db)):
    return await auth_controller.get_employee_by_id(db=db, employee_id=employee_id)


@auth_router.get("/employees/farm/{farm_id}", response_model=List[EmployeeRead])
async def get_employees_by_farm(farm_id: UUID, db: AsyncSession = Depends(get_db)):
    return await auth_controller.get_employees_by_farm(db=db, farm_id=farm_id)


@auth_router.put("/employees/{employee_id}", response_model=EmployeeRead)
async def update_employee(
    employee_id: UUID, request_data: Dict[str, Any], db: AsyncSession = Depends(get_db)
):
    return await auth_controller.update_employee(
        db=db, employee_id=employee_id, request_data=request_data
    )


@auth_router.delete("/employees/{employee_id}", status_code=status.HTTP_200_OK)
async def delete_employee(employee_id: UUID, db: AsyncSession = Depends(get_db)):
    return await auth_controller.delete_employee(db=db, employee_id=employee_id)
