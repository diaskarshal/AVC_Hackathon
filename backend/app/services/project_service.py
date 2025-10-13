from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.project import Project
from app.models.task import Task, TaskStatus
from app.schemas.project import ProjectCreate, ProjectUpdate
from datetime import datetime


class ProjectService:
    def __init__(self, db: Session):
        self.db = db
    
    def create_project(self, project: ProjectCreate) -> Project:
        db_project = Project(**project.model_dump())
        self.db.add(db_project)
        self.db.commit()
        self.db.refresh(db_project)
        return db_project
    
    def get_projects(self, skip: int = 0, limit: int = 10) -> List[Project]:
        return self.db.query(Project).offset(skip).limit(limit).all()
    
    def get_project_by_id(self, project_id: int) -> Optional[Project]:
        return self.db.query(Project).filter(Project.id == project_id).first()
    
    def update_project(self, project_id: int, project_update: ProjectUpdate) -> Optional[Project]:
        db_project = self.get_project_by_id(project_id)
        if not db_project:
            return None
        
        update_data = project_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_project, field, value)
        
        db_project.updated_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(db_project)
        return db_project
    
    def delete_project(self, project_id: int) -> bool:
        db_project = self.get_project_by_id(project_id)
        if not db_project:
            return False
        
        self.db.delete(db_project)
        self.db.commit()
        return True
    
    def get_projects_summary(self) -> List[dict]:
        """Get projects summary + progress"""
        projects = self.db.query(Project).all()
        summaries = []
        
        for project in projects:
            # Calculate progress based on completed tasks
            total_tasks = self.db.query(Task).filter(Task.project_id == project.id).count()
            completed_tasks = self.db.query(Task).filter(
                Task.project_id == project.id,
                Task.status == TaskStatus.COMPLETED
            ).count()
            
            progress = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
            
            summaries.append({
                "id": project.id,
                "name": project.name,
                "status": project.status,
                "budget_utilization": project.budget_utilization,
                "progress": round(progress, 2)
            })
        
        return summaries