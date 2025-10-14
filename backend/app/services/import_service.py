from sqlalchemy.orm import Session
import pandas as pd
from io import BytesIO
from app.models.project import Project, ProjectStatus
from app.models.task import Task, TaskStatus, TaskPriority
from app.models.resource import Resource, ResourceType, ResourceStatus
from app.models.budget import Budget
from datetime import datetime
from typing import Dict


class ImportService:
    def __init__(self, db: Session):
        self.db = db
    
    def import_from_excel(self, file_content: bytes, filename: str) -> Dict:
        """Import data from Excel file with multiple sheets"""
        try:
            excel_file = BytesIO(file_content)
            
            # Reads all sheets
            sheets = pd.read_excel(excel_file, sheet_name=None, engine='openpyxl')
            
            stats = {
                "projects": 0,
                "tasks": 0,
                "resources": 0,
                "budgets": 0
            }
            
            if 'Projects' in sheets or 'projects' in sheets:
                sheet_name = 'Projects' if 'Projects' in sheets else 'projects'
                stats["projects"] = self._import_projects(sheets[sheet_name])
            
            if 'Tasks' in sheets or 'tasks' in sheets:
                sheet_name = 'Tasks' if 'Tasks' in sheets else 'tasks'
                stats["tasks"] = self._import_tasks(sheets[sheet_name])
            
            if 'Resources' in sheets or 'resources' in sheets:
                sheet_name = 'Resources' if 'Resources' in sheets else 'resources'
                stats["resources"] = self._import_resources(sheets[sheet_name])
            
            if 'Budgets' in sheets or 'budgets' in sheets:
                sheet_name = 'Budgets' if 'Budgets' in sheets else 'budgets'
                stats["budgets"] = self._import_budgets(sheets[sheet_name])
            
            return stats
        
        except Exception as e:
            self.db.rollback()
            raise Exception(f"Error importing Excel: {str(e)}")
    
    def _import_tasks(self, df: pd.DataFrame) -> int:
        """Import tasks from dataframe"""
        count = 0
        df.columns = df.columns.str.strip().str.lower()
        
        for _, row in df.iterrows():
            try:
                name = row.get('name') or row.get('task_name', f"Task {count+1}")
                
                # Handle project_id - try to find by name first
                project_id = None
                if 'project_name' in row and pd.notna(row.get('project_name')):
                    project = self.db.query(Project).filter(
                        Project.name == str(row['project_name'])
                    ).first()
                    if project:
                        project_id = project.id
                
                if project_id is None:
                    project_id = int(row.get('project_id', 1))
                
                task = Task(
                    project_id=project_id,
                    name=str(name),
                    description=str(row.get('description', '')),
                    status=self._parse_task_status(row.get('status', 'not_started')),
                    priority=self._parse_task_priority(row.get('priority', 'medium')),
                    start_date=pd.to_datetime(row.get('start_date')) if pd.notna(row.get('start_date')) else None,
                    planned_end_date=pd.to_datetime(row.get('end_date') or row.get('planned_end_date')) if pd.notna(row.get('end_date') or row.get('planned_end_date')) else None,
                    progress_percentage=float(row.get('progress') or row.get('progress_percentage', 0)),
                    assigned_to=str(row.get('assigned_to', ''))
                )
                self.db.add(task)
                count += 1
            except Exception as e:
                print(f"Error importing task row: {e}")
                continue
        
        self.db.commit()
        return count
    
    def _import_projects(self, df: pd.DataFrame) -> int:
        """Import projects from dataframe"""
        count = 0
        df.columns = df.columns.str.strip().str.lower()
        
        for _, row in df.iterrows():
            try:
                # Handle different column name variations
                name = row.get('name') or row.get('project_name', f"Project {count+1}")
                
                project = Project(
                    name=str(name),
                    description=str(row.get('description', '')),
                    status=self._parse_project_status(row.get('status', 'planning')),
                    start_date=pd.to_datetime(row.get('start_date')) if pd.notna(row.get('start_date')) else None,
                    planned_end_date=pd.to_datetime(row.get('end_date') or row.get('planned_end_date')) if pd.notna(row.get('end_date') or row.get('planned_end_date')) else None,
                    total_budget=float(row.get('total_budget', 0)),
                    spent_amount=float(row.get('spent_amount', 0)),
                    location=str(row.get('location', ''))
                )
                self.db.add(project)
                count += 1
            except Exception as e:
                print(f"Error importing project row: {e}")
                continue
        
        self.db.commit()
        return count
    
    def _import_tasks(self, df: pd.DataFrame) -> int:
        """Import tasks from dataframe"""
        count = 0
        df.columns = df.columns.str.strip().str.lower()
        
        for _, row in df.iterrows():
            try:
                # Handle different column name variations
                name = row.get('name') or row.get('task_name', f"Task {count+1}")
                
                task = Task(
                    project_id=int(row.get('project_id', 1)),
                    name=str(name),
                    description=str(row.get('description', '')),
                    status=self._parse_task_status(row.get('status', 'not_started')),
                    priority=self._parse_task_priority(row.get('priority', 'medium')),
                    start_date=pd.to_datetime(row.get('start_date')) if pd.notna(row.get('start_date')) else None,
                    planned_end_date=pd.to_datetime(row.get('end_date') or row.get('planned_end_date')) if pd.notna(row.get('end_date') or row.get('planned_end_date')) else None,
                    progress_percentage=float(row.get('progress') or row.get('progress_percentage', 0)),
                    assigned_to=str(row.get('assigned_to', ''))
                )
                self.db.add(task)
                count += 1
            except Exception as e:
                print(f"Error importing task row: {e}")
                continue
        
        self.db.commit()
        return count
    
    def _import_resources(self, df: pd.DataFrame) -> int:
        count = 0
        df.columns = df.columns.str.strip().str.lower()
        
        for _, row in df.iterrows():
            try:
                name = row.get('name') or row.get('resource_name', f"Resource {count+1}")
                
                # Handle project_id - try to find by name first
                project_id = None
                if 'project_name' in row and pd.notna(row.get('project_name')):
                    project = self.db.query(Project).filter(
                        Project.name == str(row['project_name'])
                    ).first()
                    if project:
                        project_id = project.id
                
                if project_id is None:
                    project_id = int(row.get('project_id', 1))
                
                resource = Resource(
                    project_id=project_id,
                    name=str(name),
                    resource_type=self._parse_resource_type(row.get('resource_type', 'material')),
                    status=self._parse_resource_status(row.get('status', 'available')),
                    quantity=float(row.get('quantity', 0)),
                    unit=str(row.get('unit', 'units')),
                    unit_cost=float(row.get('unit_cost', 0)),
                    supplier=str(row.get('supplier', ''))
                )
                resource.calculate_total_cost()
                self.db.add(resource)
                count += 1
            except Exception as e:
                print(f"Error importing resource row: {e}")
                continue
        
        self.db.commit()
        return count
    
    def _import_budgets(self, df: pd.DataFrame) -> int:
        """Import budgets from dataframe"""
        count = 0
        df.columns = df.columns.str.strip().str.lower()
        
        for _, row in df.iterrows():
            try:
                # Handle project_id - try to find by name first
                project_id = None
                if 'project_name' in row and pd.notna(row.get('project_name')):
                    project = self.db.query(Project).filter(
                        Project.name == str(row['project_name'])
                    ).first()
                    if project:
                        project_id = project.id
                
                if project_id is None:
                    project_id = int(row.get('project_id', 1))
                
                budget = Budget(
                    project_id=project_id,
                    category=str(row.get('category', 'General')),
                    description=str(row.get('description', '')),
                    planned_amount=float(row.get('planned_amount', 0)),
                    actual_amount=float(row.get('actual_amount', 0))
                )
                self.db.add(budget)
                count += 1
            except Exception as e:
                print(f"Error importing budget row: {e}")
                continue
        
        self.db.commit()
        return count
    
    # Helper methods to parse enum values
    def _parse_project_status(self, status: str) -> ProjectStatus:
        status_map = {
            'planning': ProjectStatus.PLANNING,
            'in_progress': ProjectStatus.IN_PROGRESS,
            'active': ProjectStatus.IN_PROGRESS,
            'on_hold': ProjectStatus.ON_HOLD,
            'completed': ProjectStatus.COMPLETED,
            'cancelled': ProjectStatus.CANCELLED
        }
        return status_map.get(str(status).lower().strip(), ProjectStatus.PLANNING)
    
    def _parse_task_status(self, status: str) -> TaskStatus:
        status_map = {
            'not_started': TaskStatus.NOT_STARTED,
            'in_progress': TaskStatus.IN_PROGRESS,
            'active': TaskStatus.IN_PROGRESS,
            'completed': TaskStatus.COMPLETED,
            'delayed': TaskStatus.DELAYED,
            'blocked': TaskStatus.BLOCKED
        }
        return status_map.get(str(status).lower().strip(), TaskStatus.NOT_STARTED)
    
    def _parse_task_priority(self, priority: str) -> TaskPriority:
        priority_map = {
            'low': TaskPriority.LOW,
            'medium': TaskPriority.MEDIUM,
            'high': TaskPriority.HIGH,
            'critical': TaskPriority.CRITICAL
        }
        return priority_map.get(str(priority).lower().strip(), TaskPriority.MEDIUM)
    
    def _parse_resource_type(self, resource_type: str) -> ResourceType:
        type_map = {
            'material': ResourceType.MATERIAL,
            'equipment': ResourceType.EQUIPMENT,
            'labor': ResourceType.LABOR,
            'human': ResourceType.LABOR
        }
        return type_map.get(str(resource_type).lower().strip(), ResourceType.MATERIAL)
    
    def _parse_resource_status(self, status: str) -> ResourceStatus:
        status_map = {
            'available': ResourceStatus.AVAILABLE,
            'in_use': ResourceStatus.IN_USE,
            'active': ResourceStatus.IN_USE,
            'depleted': ResourceStatus.DEPLETED,
            'maintenance': ResourceStatus.MAINTENANCE,
            'ordered': ResourceStatus.AVAILABLE,
            'retired': ResourceStatus.DEPLETED
        }
        return status_map.get(str(status).lower().strip(), ResourceStatus.AVAILABLE)