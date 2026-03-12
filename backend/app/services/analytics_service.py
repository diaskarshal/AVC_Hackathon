from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.project import Project, ProjectStatus
from app.models.task import Task, TaskStatus
from app.models.resource import Resource, ResourceType
from app.models.budget import Budget
from datetime import datetime, timedelta
from typing import Dict, List


class AnalyticsService:
    def __init__(self, db: Session):
        self.db = db
    
    def get_dashboard_stats(self) -> Dict:
        total_projects = self.db.query(Project).count()
        active_projects = self.db.query(Project).filter(
            Project.status == ProjectStatus.IN_PROGRESS
        ).count()
        
        total_budget = self.db.query(func.sum(Project.total_budget)).scalar() or 0
        total_spent = self.db.query(func.sum(Project.spent_amount)).scalar() or 0
        
        total_tasks = self.db.query(Task).count()
        completed_tasks = self.db.query(Task).filter(
            Task.status == TaskStatus.COMPLETED
        ).count()
        overdue_tasks = self.db.query(Task).filter(
            Task.status != TaskStatus.COMPLETED,
            Task.planned_end_date < datetime.utcnow()
        ).count()
        
        return {
            "total_projects": total_projects,
            "active_projects": active_projects,
            "completed_projects": self.db.query(Project).filter(
                Project.status == ProjectStatus.COMPLETED
            ).count(),
            "total_budget": round(total_budget, 2),
            "total_spent": round(total_spent, 2),
            "budget_utilization": round((total_spent / total_budget * 100) if total_budget > 0 else 0, 2),
            "total_tasks": total_tasks,
            "completed_tasks": completed_tasks,
            "overdue_tasks": overdue_tasks,
            "task_completion_rate": round((completed_tasks / total_tasks * 100) if total_tasks > 0 else 0, 2)
        }
    
    def get_project_kpi(self, project_id: int) -> Dict:
        project = self.db.query(Project).filter(Project.id == project_id).first()
        if not project:
            return {}
        
        tasks = self.db.query(Task).filter(Task.project_id == project_id).all()
        total_tasks = len(tasks)
        completed_tasks = len([t for t in tasks if t.status == TaskStatus.COMPLETED])
        overdue_tasks = len([t for t in tasks if t.is_overdue])
        
        resources = self.db.query(Resource).filter(Resource.project_id == project_id).all()
        total_resource_cost = sum(r.total_cost for r in resources)
        
        return {
            "project_name": project.name,
            "status": project.status.value,
            "progress": round((completed_tasks / total_tasks * 100) if total_tasks > 0 else 0, 2),
            "budget_total": project.total_budget,
            "budget_spent": project.spent_amount,
            "budget_remaining": project.remaining_budget,
            "budget_utilization": round(project.budget_utilization, 2),
            "total_tasks": total_tasks,
            "completed_tasks": completed_tasks,
            "in_progress_tasks": len([t for t in tasks if t.status == TaskStatus.IN_PROGRESS]),
            "overdue_tasks": overdue_tasks,
            "total_resources": len(resources),
            "resource_cost": round(total_resource_cost, 2),
            "start_date": project.start_date.isoformat() if project.start_date else None,
            "planned_end": project.planned_end_date.isoformat() if project.planned_end_date else None,
            "actual_end": project.actual_end_date.isoformat() if project.actual_end_date else None
        }
    
    def get_budget_breakdown(self, project_id: int) -> List[Dict]:
        budgets = self.db.query(Budget).filter(Budget.project_id == project_id).all()
        
        breakdown = []
        for budget in budgets:
            breakdown.append({
                "category": budget.category,
                "planned": budget.planned_amount,
                "actual": budget.actual_amount,
                "variance": budget.variance,
                "variance_percentage": round(budget.variance_percentage, 2)
            })
        
        return breakdown
    
    def get_resource_distribution(self, project_id: int) -> Dict:
        resources = self.db.query(Resource).filter(Resource.project_id == project_id).all()
        
        distribution = {
            ResourceType.MATERIAL.value: {"count": 0, "total_cost": 0},
            ResourceType.EQUIPMENT.value: {"count": 0, "total_cost": 0},
            ResourceType.LABOR.value: {"count": 0, "total_cost": 0}
        }
        
        for resource in resources:
            dist_key = resource.resource_type.value
            distribution[dist_key]["count"] += 1
            distribution[dist_key]["total_cost"] += resource.total_cost
        
        return distribution
    
    def get_project_timeline(self, project_id: int) -> Dict:
        project = self.db.query(Project).filter(Project.id == project_id).first()
        if not project:
            return {}
        
        tasks = self.db.query(Task).filter(Task.project_id == project_id).order_by(Task.start_date).all()
        
        timeline = []
        for task in tasks:
            timeline.append({
                "id": task.id,
                "name": task.name,
                "status": task.status.value,
                "start_date": task.start_date.isoformat() if task.start_date else None,
                "planned_end": task.planned_end_date.isoformat() if task.planned_end_date else None,
                "actual_end": task.actual_end_date.isoformat() if task.actual_end_date else None,
                "progress": task.progress_percentage,
                "is_overdue": task.is_overdue
            })
        
        return {
            "project_name": project.name,
            "project_start": project.start_date.isoformat() if project.start_date else None,
            "project_end": project.planned_end_date.isoformat() if project.planned_end_date else None,
            "tasks": timeline
        }
    
    def predict_completion(self, project_id: int) -> Dict:
        project = self.db.query(Project).filter(Project.id == project_id).first()
        if not project:
            return {}
        
        tasks = self.db.query(Task).filter(Task.project_id == project_id).all()
        completed = len([t for t in tasks if t.status == TaskStatus.COMPLETED])
        total = len(tasks)
        
        if total == 0 or completed == 0:
            return {
                "predicted_completion_date": None,
                "predicted_total_cost": project.total_budget,
                "confidence": "low"
            }
        
        # Simple linear projection
        progress_rate = completed / total
        
        if project.start_date and progress_rate > 0:
            days_elapsed = (datetime.utcnow() - project.start_date).days
            estimated_total_days = days_elapsed / progress_rate
            predicted_date = project.start_date + timedelta(days=estimated_total_days)
        else:
            predicted_date = project.planned_end_date
        
        # Cost prediction
        if project.spent_amount > 0:
            predicted_cost = project.spent_amount / progress_rate
        else:
            predicted_cost = project.total_budget
        
        return {
            "predicted_completion_date": predicted_date.isoformat() if predicted_date else None,
            "predicted_total_cost": round(predicted_cost, 2),
            "current_progress": round(progress_rate * 100, 2),
            "cost_overrun": round(predicted_cost - project.total_budget, 2),
            "confidence": "medium" if completed > 3 else "low"
        }
    
    def get_manager_dashboard_stats(self, managed_project_ids: List[int]) -> Dict:
        if not managed_project_ids:
            return {
                "total_projects": 0,
                "active_projects": 0,
                "completed_projects": 0,
                "total_budget": 0,
                "total_spent": 0,
                "budget_utilization": 0,
                "total_tasks": 0,
                "completed_tasks": 0,
                "overdue_tasks": 0,
                "task_completion_rate": 0
            }
        
        total_projects = self.db.query(Project).filter(
            Project.id.in_(managed_project_ids)
        ).count()
        
        active_projects = self.db.query(Project).filter(
            Project.id.in_(managed_project_ids),
            Project.status == ProjectStatus.IN_PROGRESS
        ).count()
        
        total_budget = self.db.query(func.sum(Project.total_budget)).filter(
            Project.id.in_(managed_project_ids)
        ).scalar() or 0
        
        total_spent = self.db.query(func.sum(Project.spent_amount)).filter(
            Project.id.in_(managed_project_ids)
        ).scalar() or 0
        
        total_tasks = self.db.query(Task).filter(
            Task.project_id.in_(managed_project_ids)
        ).count()
        
        completed_tasks = self.db.query(Task).filter(
            Task.project_id.in_(managed_project_ids),
            Task.status == TaskStatus.COMPLETED
        ).count()
        
        overdue_tasks = self.db.query(Task).filter(
            Task.project_id.in_(managed_project_ids),
            Task.status != TaskStatus.COMPLETED,
            Task.planned_end_date < datetime.utcnow()
        ).count()
        
        return {
            "total_projects": total_projects,
            "active_projects": active_projects,
            "completed_projects": self.db.query(Project).filter(
                Project.id.in_(managed_project_ids),
                Project.status == ProjectStatus.COMPLETED
            ).count(),
            "total_budget": round(total_budget, 2),
            "total_spent": round(total_spent, 2),
            "budget_utilization": round(
                (total_spent / total_budget * 100) if total_budget > 0 else 0, 2
            ),
            "total_tasks": total_tasks,
            "completed_tasks": completed_tasks,
            "overdue_tasks": overdue_tasks,
            "task_completion_rate": round(
                (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0, 2
            )
        }


    def get_worker_dashboard_stats(self, worker_name: str) -> Dict:
        total_tasks = self.db.query(Task).filter(
            Task.assigned_to == worker_name
        ).count()
        
        completed_tasks = self.db.query(Task).filter(
            Task.assigned_to == worker_name,
            Task.status == TaskStatus.COMPLETED
        ).count()
        
        in_progress_tasks = self.db.query(Task).filter(
            Task.assigned_to == worker_name,
            Task.status == TaskStatus.IN_PROGRESS
        ).count()
        
        overdue_tasks = self.db.query(Task).filter(
            Task.assigned_to == worker_name,
            Task.status != TaskStatus.COMPLETED,
            Task.planned_end_date < datetime.utcnow()
        ).count()
        
        upcoming_deadline = datetime.utcnow() + timedelta(days=7)
        upcoming_tasks = self.db.query(Task).filter(
            Task.assigned_to == worker_name,
            Task.status != TaskStatus.COMPLETED,
            Task.planned_end_date.between(datetime.utcnow(), upcoming_deadline)
        ).count()
        
        return {
            "total_tasks": total_tasks,
            "completed_tasks": completed_tasks,
            "in_progress_tasks": in_progress_tasks,
            "not_started_tasks": self.db.query(Task).filter(
                Task.assigned_to == worker_name,
                Task.status == TaskStatus.NOT_STARTED
            ).count(),
            "overdue_tasks": overdue_tasks,
            "upcoming_tasks": upcoming_tasks,
            "task_completion_rate": round(
                (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0, 2
            )
        }

    def get_charts_data(self) -> Dict:
        projects = self.db.query(Project).all()

        plant_counts: Dict[str, int] = {}
        status_counts: Dict[str, int] = {}
        budget_per_project = []

        for project in projects:
            location = project.location or ""
            if "АНПЗ" in location:
                plant = "АНПЗ"
            elif "МНПЗ" in location:
                plant = "МНПЗ"
            elif "ПНХЗ" in location or "Павлодар" in location:
                plant = "ПНХЗ"
            else:
                plant = "Другое"
            plant_counts[plant] = plant_counts.get(plant, 0) + 1

            s = project.status.value
            status_counts[s] = status_counts.get(s, 0) + 1

            short_name = (project.name[:28] + "…") if len(project.name) > 28 else project.name
            budget_per_project.append({
                "name": short_name,
                "budget": round(project.total_budget / 1_000_000, 2),
                "spent": round(project.spent_amount / 1_000_000, 2),
            })

        return {
            "projects_by_plant": [{"label": k, "value": v} for k, v in plant_counts.items()],
            "projects_by_status": [{"label": k, "value": v} for k, v in status_counts.items()],
            "budget_vs_spent": budget_per_project,
        }

    def get_workforce_utilization(self) -> Dict:
        """Company capacity vs deployed workers across active projects."""
        TOTAL_CAPACITY = 1000  # AVC GROUP штатная численность

        active_projects = self.db.query(Project).filter(
            Project.status == ProjectStatus.IN_PROGRESS
        ).all()

        active_ids = [p.id for p in active_projects]

        # Sum labour resources per project
        project_workforce = []
        total_deployed = 0
        for p in active_projects:
            labor_resources = self.db.query(Resource).filter(
                Resource.project_id == p.id,
                Resource.resource_type == ResourceType.LABOR,
            ).all()
            workers = int(sum(r.quantity for r in labor_resources))
            total_deployed += workers
            short_name = (p.name[:25] + "…") if len(p.name) > 25 else p.name
            project_workforce.append({
                "project": short_name,
                "workers": workers,
                "budget": round(p.total_budget / 1_000_000, 1),
            })

        # Sort descending by workers
        project_workforce.sort(key=lambda x: x["workers"], reverse=True)

        utilization_pct = round(total_deployed / TOTAL_CAPACITY * 100, 1) if TOTAL_CAPACITY > 0 else 0

        return {
            "total_capacity": TOTAL_CAPACITY,
            "total_deployed": total_deployed,
            "available": max(0, TOTAL_CAPACITY - total_deployed),
            "utilization_pct": utilization_pct,
            "active_projects_count": len(active_projects),
            "by_project": project_workforce,
        }

    def get_budget_trend(self) -> Dict:
        """Monthly cumulative planned budget vs actual spent, plus a forecast line."""
        from collections import defaultdict
        import calendar

        projects = self.db.query(Project).all()

        # Build monthly buckets: { "YYYY-MM": {"planned": X, "spent": Y} }
        monthly: Dict[str, Dict[str, float]] = defaultdict(lambda: {"planned": 0.0, "spent": 0.0})

        for p in projects:
            if not p.start_date:
                continue
            # Attribute the entire planned budget to the project's start month
            month_key = p.start_date.strftime("%Y-%m")
            monthly[month_key]["planned"] += float(p.total_budget or 0)
            monthly[month_key]["spent"] += float(p.spent_amount or 0)

        if not monthly:
            return {"months": [], "planned": [], "actual": [], "forecast": []}

        # Sort months
        sorted_months = sorted(monthly.keys())
        months_out = []
        cumulative_planned = []
        cumulative_actual = []
        cum_p = 0.0
        cum_a = 0.0
        for m in sorted_months:
            cum_p += monthly[m]["planned"]
            cum_a += monthly[m]["spent"]
            months_out.append(m)
            cumulative_planned.append(round(cum_p / 1_000_000, 2))
            cumulative_actual.append(round(cum_a / 1_000_000, 2))

        # Simple forecast: linear extension from the last actual point
        # Slope = average monthly spend across all months
        n = len(months_out)
        slope = (cumulative_actual[-1] / n) if n > 0 else 0

        # Project 3 more months forward
        forecast_months = []
        forecast_values = []
        last_m = sorted_months[-1]
        year, month = int(last_m[:4]), int(last_m[5:])
        last_val = cumulative_actual[-1]
        for i in range(1, 4):
            month += 1
            if month > 12:
                month = 1
                year += 1
            forecast_months.append(f"{year:04d}-{month:02d}")
            forecast_values.append(round(last_val + slope * i, 2))

        return {
            "months": months_out,
            "planned": cumulative_planned,
            "actual": cumulative_actual,
            "forecast_months": forecast_months,
            "forecast": forecast_values,
        }

    def get_team_performance(self, project_id: int = None) -> Dict:
        from sqlalchemy import case
        
        query = self.db.query(
            Task.assigned_to,
            func.count(Task.id).label("total_tasks"),
            func.sum(
                case(
                    (Task.status == TaskStatus.COMPLETED, 1),
                    else_=0
                )
            ).label("completed_tasks"),
            func.avg(Task.progress_percentage).label("avg_progress")
        ).filter(Task.assigned_to.isnot(None))
        
        if project_id:
            query = query.filter(Task.project_id == project_id)
        
        results = query.group_by(Task.assigned_to).all()
        
        team_stats = []
        for result in results:
            completion_rate = (
                (result.completed_tasks / result.total_tasks * 100)
                if result.total_tasks > 0 else 0
            )
            team_stats.append({
                "worker_name": result.assigned_to,
                "total_tasks": result.total_tasks,
                "completed_tasks": result.completed_tasks,
                "avg_progress": round(result.avg_progress or 0, 2),
                "completion_rate": round(completion_rate, 2)
            })
        
        return {
            "team_members": len(team_stats),
            "performance": team_stats
        }