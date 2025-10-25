from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any
import uuid
import bcrypt
from jose import jwt

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from chavfana.models.user import User, Employee
from chavfana.schemas.user import UserCreate, UserUpdate, UserRead, EmployeeCreate, EmployeeRead
from chavfana.core.exceptions import NotFoundError, BusinessLogicError, AuthenticationError, DatabaseIntegrityError
from chavfana.core.logging import logger
from chavfana.core.config import settings


class AuthController:
    @staticmethod
    def hash_password(password: str) -> str:
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode(), salt).decode()

    @staticmethod
    def verify_password(password: str, password_hash: str) -> bool:
        return bcrypt.checkpw(password.encode(), password_hash.encode())

    @staticmethod
    def create_access_token(user_id: uuid.UUID, role: str) -> str:
        payload = {
            "sub": str(user_id),
            "role": role,
            "exp": datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
            "iat": datetime.now(timezone.utc),
        }
        return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

    @staticmethod
    async def create_user(db: AsyncSession, request_data: UserCreate) -> UserRead:
        try:
            existing_user = await db.execute(
                select(User).where(User.email == request_data.email)
            )
            if existing_user.scalar_one_or_none():
                raise BusinessLogicError(message="Email already registered")

            hashed_password = AuthController.hash_password(request_data.password)
            
            new_user = User(
                email=request_data.email,
                full_name=request_data.full_name,
                phone=request_data.phone,
                role=request_data.role,
                password_hash=hashed_password,
                profile_data=request_data.profile_data,
            )
            
            db.add(new_user)
            await db.flush()
            await db.refresh(new_user)
            
            logger.info(f"User created: {new_user.email} with role {new_user.role}")
            return UserRead.model_validate(new_user)
        except BusinessLogicError:
            raise
        except Exception as e:
            logger.error(f"Error creating user: {str(e)}")
            raise DatabaseIntegrityError(message="Failed to create user")

    @staticmethod
    async def login(db: AsyncSession, email: str, password: str) -> Dict[str, Any]:
        try:
            result = await db.execute(
                select(User).where(User.email == email)
            )
            user = result.scalar_one_or_none()
            
            if not user:
                raise AuthenticationError(message="Invalid email or password")
            
            if not user.is_active:
                raise AuthenticationError(message="User account is inactive")
            
            if not AuthController.verify_password(password, user.password_hash):
                raise AuthenticationError(message="Invalid email or password")
            
            user.last_login = datetime.now(timezone.utc)
            await db.flush()
            await db.refresh(user)
            
            access_token = AuthController.create_access_token(user.id, user.role)
            
            logger.info(f"User logged in: {user.email}")
            return {
                "access_token": access_token,
                "token_type": "bearer",
                "user": UserRead.model_validate(user, from_attributes=True),
            }
        except AuthenticationError:
            raise
        except Exception as e:
            logger.error(f"Error during login: {str(e)}")
            raise AuthenticationError(message="Login failed")

    @staticmethod
    async def get_user_by_id(db: AsyncSession, user_id: uuid.UUID) -> UserRead:
        try:
            result = await db.execute(
                select(User).where(User.id == user_id)
            )
            user = result.scalar_one_or_none()
            
            if not user:
                raise NotFoundError(resource_type="User", resource_id=str(user_id))
            
            return UserRead.model_validate(user)
        except NotFoundError:
            raise
        except Exception as e:
            logger.error(f"Error fetching user: {str(e)}")
            raise

    @staticmethod
    async def get_user_by_email(db: AsyncSession, email: str) -> UserRead:
        try:
            result = await db.execute(
                select(User).where(User.email == email)
            )
            user = result.scalar_one_or_none()
            
            if not user:
                raise NotFoundError(resource_type="User", resource_id=email)
            
            return UserRead.model_validate(user)
        except NotFoundError:
            raise
        except Exception as e:
            logger.error(f"Error fetching user by email: {str(e)}")
            raise

    @staticmethod
    async def update_user(db: AsyncSession, user_id: uuid.UUID, request_data: UserUpdate) -> UserRead:
        try:
            result = await db.execute(
                select(User).where(User.id == user_id)
            )
            user = result.scalar_one_or_none()
            
            if not user:
                raise NotFoundError(resource_type="User", resource_id=str(user_id))
            
            update_data = request_data.model_dump(exclude_unset=True)
            
            if "email" in update_data and update_data["email"] != user.email:
                existing = await db.execute(
                    select(User).where(User.email == update_data["email"])
                )
                if existing.scalar_one_or_none():
                    raise BusinessLogicError(message="Email already in use")
            
            for field, value in update_data.items():
                setattr(user, field, value)
            
            await db.flush()
            await db.refresh(user)
            
            logger.info(f"User updated: {user.email}")
            return UserRead.model_validate(user)
        except (NotFoundError, BusinessLogicError):
            raise
        except Exception as e:
            logger.error(f"Error updating user: {str(e)}")
            raise DatabaseIntegrityError(message="Failed to update user")

    @staticmethod
    async def deactivate_user(db: AsyncSession, user_id: uuid.UUID) -> UserRead:
        try:
            result = await db.execute(
                select(User).where(User.id == user_id)
            )
            user = result.scalar_one_or_none()
            
            if not user:
                raise NotFoundError(resource_type="User", resource_id=str(user_id))
            
            user.is_active = False
            await db.flush()
            await db.refresh(user)
            
            logger.info(f"User deactivated: {user.email}")
            return UserRead.model_validate(user)
        except NotFoundError:
            raise
        except Exception as e:
            logger.error(f"Error deactivating user: {str(e)}")
            raise DatabaseIntegrityError(message="Failed to deactivate user")

    @staticmethod
    async def activate_user(db: AsyncSession, user_id: uuid.UUID) -> UserRead:
        try:
            result = await db.execute(
                select(User).where(User.id == user_id)
            )
            user = result.scalar_one_or_none()
            
            if not user:
                raise NotFoundError(resource_type="User", resource_id=str(user_id))
            
            user.is_active = True
            await db.flush()
            await db.refresh(user)
            
            logger.info(f"User activated: {user.email}")
            return UserRead.model_validate(user)
        except NotFoundError:
            raise
        except Exception as e:
            logger.error(f"Error activating user: {str(e)}")
            raise DatabaseIntegrityError(message="Failed to activate user")

    @staticmethod
    async def change_password(db: AsyncSession, user_id: uuid.UUID, old_password: str, new_password: str) -> Dict[str, str]:
        try:
            result = await db.execute(
                select(User).where(User.id == user_id)
            )
            user = result.scalar_one_or_none()
            
            if not user:
                raise NotFoundError(resource_type="User", resource_id=str(user_id))
            
            if not AuthController.verify_password(old_password, user.password_hash):
                raise AuthenticationError(message="Current password is incorrect")
            
            user.password_hash = AuthController.hash_password(new_password)
            await db.flush()
            
            logger.info(f"Password changed for user: {user.email}")
            return {"message": "Password changed successfully"}
        except (NotFoundError, AuthenticationError):
            raise
        except Exception as e:
            logger.error(f"Error changing password: {str(e)}")
            raise DatabaseIntegrityError(message="Failed to change password")

    @staticmethod
    async def get_all_users(db: AsyncSession, skip: int = 0, limit: int = 100) -> list[UserRead]:
        try:
            result = await db.execute(
                select(User).offset(skip).limit(limit)
            )
            users = result.scalars().all()
            return [UserRead.model_validate(user) for user in users]
        except Exception as e:
            logger.error(f"Error fetching users: {str(e)}")
            raise

    @staticmethod
    async def get_users_by_role(db: AsyncSession, role: str, skip: int = 0, limit: int = 100) -> list[UserRead]:
        try:
            result = await db.execute(
                select(User).where(User.role == role).offset(skip).limit(limit)
            )
            users = result.scalars().all()
            return [UserRead.model_validate(user) for user in users]
        except Exception as e:
            logger.error(f"Error fetching users by role: {str(e)}")
            raise

    @staticmethod
    async def create_employee(db: AsyncSession, request_data: EmployeeCreate) -> EmployeeRead:
        try:
            result = await db.execute(
                select(User).where(User.id == request_data.user_id)
            )
            if not result.scalar_one_or_none():
                raise NotFoundError(resource_type="User", resource_id=str(request_data.user_id))
            
            new_employee = Employee(
                user_id=request_data.user_id,
                farm_id=request_data.farm_id,
                position=request_data.position,
                employment_start=request_data.employment_start,
                employment_end=request_data.employment_end,
                salary_amount=request_data.salary_amount,
                salary_currency=request_data.salary_currency,
            )
            
            db.add(new_employee)
            await db.flush()
            await db.refresh(new_employee)
            
            logger.info(f"Employee created: {new_employee.id}")
            return EmployeeRead.model_validate(new_employee)
        except NotFoundError:
            raise
        except Exception as e:
            logger.error(f"Error creating employee: {str(e)}")
            raise DatabaseIntegrityError(message="Failed to create employee")

    @staticmethod
    async def get_employee_by_id(db: AsyncSession, employee_id: uuid.UUID) -> EmployeeRead:
        try:
            result = await db.execute(
                select(Employee).where(Employee.id == employee_id)
            )
            employee = result.scalar_one_or_none()
            
            if not employee:
                raise NotFoundError(resource_type="Employee", resource_id=str(employee_id))
            
            return EmployeeRead.model_validate(employee)
        except NotFoundError:
            raise
        except Exception as e:
            logger.error(f"Error fetching employee: {str(e)}")
            raise

    @staticmethod
    async def get_employees_by_farm(db: AsyncSession, farm_id: uuid.UUID) -> list[EmployeeRead]:
        try:
            result = await db.execute(
                select(Employee).where(Employee.farm_id == farm_id)
            )
            employees = result.scalars().all()
            return [EmployeeRead.model_validate(emp) for emp in employees]
        except Exception as e:
            logger.error(f"Error fetching employees by farm: {str(e)}")
            raise

    @staticmethod
    async def update_employee(db: AsyncSession, employee_id: uuid.UUID, request_data: Dict[str, Any]) -> EmployeeRead:
        try:
            result = await db.execute(
                select(Employee).where(Employee.id == employee_id)
            )
            employee = result.scalar_one_or_none()
            
            if not employee:
                raise NotFoundError(resource_type="Employee", resource_id=str(employee_id))
            
            for field, value in request_data.items():
                if value is not None:
                    setattr(employee, field, value)
            
            await db.flush()
            await db.refresh(employee)
            
            logger.info(f"Employee updated: {employee.id}")
            return EmployeeRead.model_validate(employee)
        except NotFoundError:
            raise
        except Exception as e:
            logger.error(f"Error updating employee: {str(e)}")
            raise DatabaseIntegrityError(message="Failed to update employee")

    @staticmethod
    async def delete_employee(db: AsyncSession, employee_id: uuid.UUID) -> Dict[str, str]:
        try:
            result = await db.execute(
                select(Employee).where(Employee.id == employee_id)
            )
            employee = result.scalar_one_or_none()
            
            if not employee:
                raise NotFoundError(resource_type="Employee", resource_id=str(employee_id))
            
            await db.delete(employee)
            await db.flush()
            
            logger.info(f"Employee deleted: {employee_id}")
            return {"message": "Employee deleted successfully"}
        except NotFoundError:
            raise
        except Exception as e:
            logger.error(f"Error deleting employee: {str(e)}")
            raise DatabaseIntegrityError(message="Failed to delete employee")
