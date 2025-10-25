from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta

from chavfana.models import (
    Farm,
    Project,
    PlantingProject,
    AnimalKeepingProject,
    Animal,
    AnimalGroup,
    Transaction,
    Task,
    DailyEntry,
    User,
    Employee,
    SoilAnalysis,
    WeatherObservation,
    CropSpecies,
    VeterinaryVisit,
)
from chavfana.core.exceptions import DatabaseError


class StatisticsController:
    @staticmethod
    async def get_all_statistics(db: AsyncSession):
        try:

            farms_count = (await db.scalar(select(func.count(Farm.id)))) or 0
            avg_farm_size = (await db.scalar(select(func.avg(Farm.area_size)))) or 0.0
            total_farm_area = (await db.scalar(select(func.sum(Farm.area_size)))) or 0.0

            total_projects = (await db.scalar(select(func.count(Project.id)))) or 0
            active_projects = (
                await db.scalar(select(func.count()).where(Project.status == "Active"))
            ) or 0
            completed_projects = (
                await db.scalar(
                    select(func.count()).where(Project.status == "Completed")
                )
            ) or 0

            planting_projects = (
                await db.scalar(select(func.count(PlantingProject.project_id)))
            ) or 0
            total_planted_area = (
                await db.scalar(
                    select(func.sum(func.coalesce(PlantingProject.expected_yield, 0)))
                )
            ) or 0
            avg_expected_revenue = (
                await db.scalar(select(func.avg(PlantingProject.expected_revenue)))
            ) or 0

            total_animals = (await db.scalar(select(func.count(Animal.id)))) or 0
            active_animals = (
                await db.scalar(select(func.count()).where(Animal.is_active.is_(True)))
            ) or 0
            avg_animal_weight = (await db.scalar(select(func.avg(Animal.weight)))) or 0
            health_distribution = {
                status: count
                for status, count in (
                    await db.execute(
                        select(Animal.health_status, func.count()).group_by(
                            Animal.health_status
                        )
                    )
                ).all()
            }

            total_transactions = (
                await db.scalar(select(func.count(Transaction.id)))
            ) or 0
            income_total = (
                await db.scalar(
                    select(func.sum(Transaction.amount)).where(
                        Transaction.transaction_type == "INCOME"
                    )
                )
            ) or 0
            expense_total = (
                await db.scalar(
                    select(func.sum(Transaction.amount)).where(
                        Transaction.transaction_type == "EXPENSE"
                    )
                )
            ) or 0
            net_balance = income_total - expense_total

            soil_stats = (
                await db.execute(
                    select(
                        func.avg(SoilAnalysis.soil_ph),
                        func.avg(SoilAnalysis.nitrogen),
                        func.avg(SoilAnalysis.organic_matter),
                    )
                )
            ).first()
            soil_summary = {
                "avg_ph": soil_stats[0],
                "avg_nitrogen": soil_stats[1],
                "avg_organic_matter": soil_stats[2],
            }

            thirty_days_ago = datetime.utcnow() - timedelta(days=30)
            weather_stats = (
                await db.execute(
                    select(
                        func.avg(WeatherObservation.temperature),
                        func.avg(WeatherObservation.humidity),
                        func.sum(WeatherObservation.rainfall_mm),
                    ).where(WeatherObservation.observed_at >= thirty_days_ago)
                )
            ).first()
            weather_summary = {
                "avg_temperature": weather_stats[0],
                "avg_humidity": weather_stats[1],
                "total_rainfall_mm": weather_stats[2],
            }

            task_counts = {
                status: count
                for status, count in (
                    await db.execute(
                        select(Task.status, func.count()).group_by(Task.status)
                    )
                ).all()
            }

            user_roles = {
                role: count
                for role, count in (
                    await db.execute(
                        select(User.role, func.count()).group_by(User.role)
                    )
                ).all()
            }
            active_users = (
                await db.scalar(select(func.count()).where(User.is_active.is_(True)))
            ) or 0

            employee_count = (await db.scalar(select(func.count(Employee.id)))) or 0
            avg_salary = (
                await db.scalar(select(func.avg(Employee.salary_amount)))
            ) or 0

            vet_visits_count = (
                await db.scalar(select(func.count(VeterinaryVisit.id)))
            ) or 0
            avg_vet_cost = (
                await db.scalar(select(func.avg(VeterinaryVisit.cost)))
            ) or 0

            return {
                "farms": {
                    "count": farms_count,
                    "avg_size": avg_farm_size,
                    "total_area": total_farm_area,
                },
                "projects": {
                    "total": total_projects,
                    "active": active_projects,
                    "completed": completed_projects,
                    "planting_projects": planting_projects,
                    "total_planted_area": total_planted_area,
                    "avg_expected_revenue": avg_expected_revenue,
                },
                "animals": {
                    "total": total_animals,
                    "active": active_animals,
                    "avg_weight": avg_animal_weight,
                    "health_distribution": health_distribution,
                },
                "finance": {
                    "transactions": total_transactions,
                    "income_total": income_total,
                    "expense_total": expense_total,
                    "net_balance": net_balance,
                },
                "soil": soil_summary,
                "weather_30d": weather_summary,
                "tasks": task_counts,
                "users": {
                    "active": active_users,
                    "roles": user_roles,
                },
                "employees": {
                    "count": employee_count,
                    "avg_salary": avg_salary,
                },
                "veterinary": {
                    "total_visits": vet_visits_count,
                    "avg_cost": avg_vet_cost,
                },
            }

        except Exception as e:
            raise DatabaseError(f"Failed to compute statistics: {e}")
