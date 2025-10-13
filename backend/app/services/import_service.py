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
            
            # Import projects
            if 'Projects' in sheets or 'projects' in sheets:
                sheet_name = 'Projects' if 'Projects' in sheets else 'projects'
                stats["projects"] = self._import_projects(sheets[sheet_name])
            
            # Import tasks
            if 'Tasks' in sheets or 'tasks' in sheets:
                sheet_name = 'Tasks' if 'Tasks' in sheets else 'tasks'
                stats["tasks"] = self._import_tasks(sheets[sheet_name])
            
            # Import resources
            if 'Resources' in sheets or 'resources' in sheets:
                sheet_name = 'Resources' if 'Resources' in sheets else 'resources'
                stats["resources"] = self._import_resources(sheets[sheet_name])
            
            # Import budgets
            if 'Budgets' in sheets or 'budgets' in sheets:
                sheet_name = 'Budgets' if 'Budgets' in sheets else 'budgets'
                stats["budgets"] = self._import_budgets(sheets[sheet_name])
            
            return stats
        
        except Exception as e:
            self.db.rollback()
            raise Exception(f"Error importing Excel: {str(e)}")
    
    def import_from_csv(self, file_content: bytes) -> Dict:
        try:
            df = pd.read_csv(BytesIO(file_content))
            
            # Detect what type of data is in the CSV based on columns
            columns = set(df.columns.str.lower())
            
            if 'project_name' in columns or 'name' in columns:
                count = self._import_projects(df)
                return {"projects": count}
            elif 'task_name' in columns:
                count = self._import_tasks(df)
                return {"tasks": count}
            elif 'resource_name' in columns or 'resource_type' in columns:
                count = self._import_resources(df)
                return {"resources": count}
            else:
                raise Exception("Unable to determine CSV data type")
        
        except Exception as e:
            self.db.rollback()
            raise Exception(f"Error importing CSV: {str(e)}")
    
    def _import_projects(self, df: pd.DataFrame) -> int:
        """Import projects from dataframe"""
        count = 0
        for _, row in df.iterrows():
            try:
                project = Project(
                    name=row.get('name') or row.get('project_name', f"Project {count+1}"),
                    description=row.get('description', ''),
                    status=ProjectStatus(row.get('status', 'planning').lower()),
                    start_date=pd.to_datetime(row.get('start_date')) if pd.notna(row.get('start_date')) else None,
                    planned_end_date=pd.to_datetime(row.get('end_date')) if pd.notna(row.get('end_date')) else None,
                    total_budget=float(row.get('total_budget', 0)),
                    spent_amount=float(row.get('spent_amount', 0)),
                    location=row.get('location', '')
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
        for _, row in df.iterrows():
            try:
                task = Task(
                    project_id=int(row.get('project_id', 1)),
                    name=row.get('name') or row.get('task_name', f"Task {count+1}"),
                    description=row.get('description', ''),
                    status=TaskStatus(row.get('status', 'not_started').lower()),
                    priority=TaskPriority(row.get('priority', 'medium').lower()),
                    start_date=pd.to_datetime(row.get('start_date')) if pd.notna(row.get('start_date')) else None,
                    planned_end_date=pd.to_datetime(row.get('end_date')) if pd.notna(row.get('end_date')) else None,
                    progress_percentage=float(row.get('progress', 0)),
                    assigned_to=row.get('assigned_to', '')
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
        for _, row in df.iterrows():
            try:
                resource = Resource(
                    project_id=int(row.get('project_id', 1)),
                    name=row.get('name') or row.get('resource_name', f"Resource {count+1}"),
                    resource_type=ResourceType(row.get('resource_type', 'material').lower()),
                    status=ResourceStatus(row.get('status', 'available').lower()),
                    quantity=float(row.get('quantity', 0)),
                    unit=row.get('unit', 'units'),
                    unit_cost=float(row.get('unit_cost', 0)),
                    supplier=row.get('supplier', '')
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
        for _, row in df.iterrows():
            try:
                budget = Budget(
                    project_id=int(row.get('project_id', 1)),
                    category=row.get('category', 'General'),
                    description=row.get('description', ''),
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