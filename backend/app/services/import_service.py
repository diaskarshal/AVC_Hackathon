from sqlalchemy.orm import Session
import pandas as pd
from io import BytesIO
from app.models.project import Project, ProjectStatus
from app.models.task import Task, TaskStatus, TaskPriority
from app.models.resource import Resource, ResourceType, ResourceStatus
from app.models.budget import Budget
from datetime import datetime
from typing import Dict, Optional


class ImportService:
    def __init__(self, db: Session):
        self.db = db
        self._project_name_to_id: Dict[str, int] = {}
    
    def _build_project_mapping(self):
        projects = self.db.query(Project).all()
        self._project_name_to_id = {
            project.name.lower().strip(): project.id 
            for project in projects
        }
    
    def _get_project_id(
        self, 
        row: pd.Series, 
        row_index: int
    ) -> Optional[int]:
        if pd.notna(row.get('project_id')):
            try:
                project_id = int(row.get('project_id'))
                exists = self.db.query(Project).filter(
                    Project.id == project_id
                ).first()
                if exists:
                    return project_id
                else:
                    print(
                        f"Row {row_index}: project_id {project_id} "
                        f"not found in database"
                    )
            except:
                print(f"Row {row_index}: Invalid project_id format")
        
        if pd.notna(row.get('project_name')):
            project_name = str(row.get('project_name')).lower().strip()
            if project_name in self._project_name_to_id:
                return self._project_name_to_id[project_name]
            else:
                print(
                    f"Row {row_index}: project_name '{project_name}' "
                    f"not found in database"
                )
        
        return None
    
    def import_from_excel(self, file_content: bytes, filename: str) -> Dict:
        try:
            excel_file = BytesIO(file_content)
            
            sheets = pd.read_excel(
                excel_file, sheet_name=None, engine='openpyxl'
            )
            
            stats = {
                "projects": 0,
                "tasks": 0,
                "resources": 0,
                "budgets": 0
            }
            
            if 'Projects' in sheets or 'projects' in sheets:
                sheet_name = 'Projects' if 'Projects' in sheets else 'projects'
                stats["projects"] = self._import_projects(sheets[sheet_name])
            
            self._build_project_mapping()
            
            if 'Tasks' in sheets or 'tasks' in sheets:
                sheet_name = 'Tasks' if 'Tasks' in sheets else 'tasks'
                stats["tasks"] = self._import_tasks(sheets[sheet_name])
            
            if 'Resources' in sheets or 'resources' in sheets:
                sheet_name = (
                    'Resources' if 'Resources' in sheets else 'resources'
                )
                stats["resources"] = self._import_resources(
                    sheets[sheet_name]
                )
            
            if 'Budgets' in sheets or 'budgets' in sheets:
                sheet_name = 'Budgets' if 'Budgets' in sheets else 'budgets'
                stats["budgets"] = self._import_budgets(sheets[sheet_name])
            
            return stats
        
        except Exception as e:
            self.db.rollback()
            raise Exception(f"Error importing Excel: {str(e)}")
    
    def import_from_csv(self, file_content: bytes) -> Dict:
        try:
            df = None
            for delimiter in [',', ';', '\t']:
                try:
                    df = pd.read_csv(BytesIO(file_content), delimiter=delimiter)
                    if len(df.columns) > 1:
                        break
                except:
                    continue
            
            if df is None or len(df.columns) <= 1:
                raise Exception("Unable to parse CSV file")
            
            df.columns = df.columns.str.strip().str.lower()
            columns = set(df.columns)
            
            if 'category' in columns and 'planned_amount' in columns:
                self._build_project_mapping()
                count = self._import_budgets(df)
                return {
                    "projects": 0,
                    "tasks": 0,
                    "resources": 0,
                    "budgets": count
                }
            elif 'resource_name' in columns or 'resource_type' in columns:
                self._build_project_mapping()
                count = self._import_resources(df)
                return {
                    "projects": 0,
                    "tasks": 0,
                    "resources": count,
                    "budgets": 0
                }
            
            elif 'task_name' in columns or (
                'name' in columns and (
                    'assigned_to' in columns or 
                    'priority' in columns or
                    'progress' in columns or
                    'progress_percentage' in columns
                )
            ):
                self._build_project_mapping()
                count = self._import_tasks(df)
                return {
                    "projects": 0,
                    "tasks": count,
                    "resources": 0,
                    "budgets": 0
                }
            
            elif 'project_name' in columns or (
                'name' in columns and 'total_budget' in columns
            ):
                count = self._import_projects(df)
                return {
                    "projects": count,
                    "tasks": 0,
                    "resources": 0,
                    "budgets": 0
                }
            
            else:
                raise Exception(
                    f"Unable to determine CSV data type. "
                    f"Columns found: {', '.join(columns)}"
                )
        
        except Exception as e:
            self.db.rollback()
            raise Exception(f"Error importing CSV: {str(e)}")
    
    def _import_projects(self, df: pd.DataFrame) -> int:
        count = 0
        df.columns = df.columns.str.strip().str.lower()
        
        for index, row in df.iterrows():
            try:
                name = row.get('name') or row.get('project_name')
                if pd.isna(name):
                    print(f"Skipping row {index}: missing project name")
                    continue
                
                name = str(name).strip()
                if not name:
                    print(f"Skipping row {index}: empty project name")
                    continue
                
                description = ''
                if pd.notna(row.get('description')):
                    description = str(row.get('description')).strip()
                
                start_date = None
                if pd.notna(row.get('start_date')):
                    try:
                        start_date = pd.to_datetime(row.get('start_date'))
                    except:
                        print(
                            f"Row {index}: Invalid start_date, skipping"
                        )
                
                planned_end_date = None
                end_date_field = row.get('end_date') or row.get(
                    'planned_end_date'
                )
                if pd.notna(end_date_field):
                    try:
                        planned_end_date = pd.to_datetime(end_date_field)
                    except:
                        print(
                            f"Row {index}: Invalid end_date, skipping"
                        )
                
                total_budget = 0.0
                if pd.notna(row.get('total_budget')):
                    try:
                        total_budget = float(row.get('total_budget'))
                    except:
                        print(
                            f"Row {index}: Invalid total_budget, using 0.0"
                        )
                
                spent_amount = 0.0
                if pd.notna(row.get('spent_amount')):
                    try:
                        spent_amount = float(row.get('spent_amount'))
                    except:
                        print(
                            f"Row {index}: Invalid spent_amount, using 0.0"
                        )
                
                location = ''
                if pd.notna(row.get('location')):
                    location = str(row.get('location')).strip()
                
                project = Project(
                    name=name,
                    description=description,
                    status=self._parse_project_status(
                        row.get('status', 'planning')
                    ),
                    start_date=start_date,
                    planned_end_date=planned_end_date,
                    total_budget=total_budget,
                    spent_amount=spent_amount,
                    location=location
                )
                self.db.add(project)
                self.db.flush()
                count += 1
            except Exception as e:
                print(f"Error importing project row {index}: {e}")
                continue
        
        self.db.commit()
        return count
    
    def _import_tasks(self, df: pd.DataFrame) -> int:
        count = 0
        df.columns = df.columns.str.strip().str.lower()
        
        for index, row in df.iterrows():
            try:
                name = row.get('name') or row.get('task_name')
                if pd.isna(name):
                    print(f"Skipping row {index}: missing task name")
                    continue
                
                name = str(name).strip()
                if not name:
                    print(f"Skipping row {index}: empty task name")
                    continue
                
                project_id = self._get_project_id(row, index)
                if project_id is None:
                    print(
                        f"Skipping row {index}: could not resolve project. "
                        f"Use 'project_id' or 'project_name' column."
                    )
                    continue
                
                description = ''
                if pd.notna(row.get('description')):
                    description = str(row.get('description')).strip()
                
                start_date = None
                if pd.notna(row.get('start_date')):
                    try:
                        start_date = pd.to_datetime(row.get('start_date'))
                    except:
                        print(f"Row {index}: Invalid start_date")
                
                planned_end_date = None
                end_date_field = row.get('end_date') or row.get(
                    'planned_end_date'
                )
                if pd.notna(end_date_field):
                    try:
                        planned_end_date = pd.to_datetime(end_date_field)
                    except:
                        print(f"Row {index}: Invalid end_date")
                
                progress = 0.0
                progress_field = row.get('progress') or row.get(
                    'progress_percentage'
                )
                if pd.notna(progress_field):
                    try:
                        progress = float(progress_field)
                        progress = max(0.0, min(100.0, progress))
                    except:
                        print(
                            f"Row {index}: Invalid progress, using 0.0"
                        )
                
                assigned_to = ''
                if pd.notna(row.get('assigned_to')):
                    assigned_to = str(row.get('assigned_to')).strip()
                
                task = Task(
                    project_id=project_id,
                    name=name,
                    description=description,
                    status=self._parse_task_status(
                        row.get('status', 'not_started')
                    ),
                    priority=self._parse_task_priority(
                        row.get('priority', 'medium')
                    ),
                    start_date=start_date,
                    planned_end_date=planned_end_date,
                    progress_percentage=progress,
                    assigned_to=assigned_to
                )
                self.db.add(task)
                count += 1
            except Exception as e:
                print(f"Error importing task row {index}: {e}")
                continue
        
        self.db.commit()
        return count
    
    def _import_resources(self, df: pd.DataFrame) -> int:
        count = 0
        df.columns = df.columns.str.strip().str.lower()
        
        for index, row in df.iterrows():
            try:
                name = row.get('name') or row.get('resource_name')
                if pd.isna(name):
                    print(f"Skipping row {index}: missing resource name")
                    continue
                
                name = str(name).strip()
                if not name:
                    print(f"Skipping row {index}: empty resource name")
                    continue
                
                project_id = self._get_project_id(row, index)
                if project_id is None:
                    print(
                        f"Skipping row {index}: could not resolve project. "
                        f"Use 'project_id' or 'project_name' column."
                    )
                    continue
                
                quantity = 0.0
                if pd.notna(row.get('quantity')):
                    try:
                        quantity = float(row.get('quantity'))
                        quantity = max(0.0, quantity)
                    except:
                        print(f"Row {index}: Invalid quantity, using 0.0")
                
                unit = 'units'
                if pd.notna(row.get('unit')):
                    unit = str(row.get('unit')).strip()
                
                unit_cost = 0.0
                if pd.notna(row.get('unit_cost')):
                    try:
                        unit_cost = float(row.get('unit_cost'))
                        unit_cost = max(0.0, unit_cost)
                    except:
                        print(f"Row {index}: Invalid unit_cost, using 0.0")
                
                supplier = ''
                if pd.notna(row.get('supplier')):
                    supplier = str(row.get('supplier')).strip()
                
                resource = Resource(
                    project_id=project_id,
                    name=name,
                    resource_type=self._parse_resource_type(
                        row.get('resource_type', 'material')
                    ),
                    status=self._parse_resource_status(
                        row.get('status', 'available')
                    ),
                    quantity=quantity,
                    unit=unit,
                    unit_cost=unit_cost,
                    supplier=supplier
                )
                resource.calculate_total_cost()
                self.db.add(resource)
                count += 1
            except Exception as e:
                print(f"Error importing resource row {index}: {e}")
                continue
        
        self.db.commit()
        return count
    
    def _import_budgets(self, df: pd.DataFrame) -> int:
        count = 0
        df.columns = df.columns.str.strip().str.lower()
        
        for index, row in df.iterrows():
            try:
                category = row.get('category')
                if pd.isna(category):
                    print(f"Skipping row {index}: missing category")
                    continue
                
                category = str(category).strip()
                if not category:
                    print(f"Skipping row {index}: empty category")
                    continue
                
                project_id = self._get_project_id(row, index)
                if project_id is None:
                    print(
                        f"Skipping row {index}: could not resolve project. "
                        f"Use 'project_id' or 'project_name' column."
                    )
                    continue
                
                description = ''
                if pd.notna(row.get('description')):
                    description = str(row.get('description')).strip()
                
                planned_amount = 0.0
                if pd.notna(row.get('planned_amount')):
                    try:
                        planned_amount = float(row.get('planned_amount'))
                        planned_amount = max(0.0, planned_amount)
                    except:
                        print(
                            f"Row {index}: Invalid planned_amount, using 0.0"
                        )
                
                actual_amount = 0.0
                if pd.notna(row.get('actual_amount')):
                    try:
                        actual_amount = float(row.get('actual_amount'))
                        actual_amount = max(0.0, actual_amount)
                    except:
                        print(
                            f"Row {index}: Invalid actual_amount, using 0.0"
                        )
                
                budget = Budget(
                    project_id=project_id,
                    category=category,
                    description=description,
                    planned_amount=planned_amount,
                    actual_amount=actual_amount
                )
                self.db.add(budget)
                count += 1
            except Exception as e:
                print(f"Error importing budget row {index}: {e}")
                continue
        
        self.db.commit()
        return count
    
    def _parse_project_status(self, status: str) -> ProjectStatus:
        if pd.isna(status):
            return ProjectStatus.PLANNING
        
        status_map = {
            'planning': ProjectStatus.PLANNING,
            'in_progress': ProjectStatus.IN_PROGRESS,
            'active': ProjectStatus.IN_PROGRESS,
            'on_hold': ProjectStatus.ON_HOLD,
            'completed': ProjectStatus.COMPLETED,
            'cancelled': ProjectStatus.CANCELLED
        }
        return status_map.get(
            str(status).lower().strip(), ProjectStatus.PLANNING
        )
    
    def _parse_task_status(self, status: str) -> TaskStatus:
        if pd.isna(status):
            return TaskStatus.NOT_STARTED
        
        status_map = {
            'not_started': TaskStatus.NOT_STARTED,
            'in_progress': TaskStatus.IN_PROGRESS,
            'active': TaskStatus.IN_PROGRESS,
            'completed': TaskStatus.COMPLETED,
            'delayed': TaskStatus.DELAYED,
            'blocked': TaskStatus.BLOCKED
        }
        return status_map.get(
            str(status).lower().strip(), TaskStatus.NOT_STARTED
        )
    
    def _parse_task_priority(self, priority: str) -> TaskPriority:
        if pd.isna(priority):
            return TaskPriority.MEDIUM
        
        priority_map = {
            'low': TaskPriority.LOW,
            'medium': TaskPriority.MEDIUM,
            'high': TaskPriority.HIGH,
            'critical': TaskPriority.CRITICAL
        }
        return priority_map.get(
            str(priority).lower().strip(), TaskPriority.MEDIUM
        )
    
    def _parse_resource_type(self, resource_type: str) -> ResourceType:
        if pd.isna(resource_type):
            return ResourceType.MATERIAL
        
        type_map = {
            'material': ResourceType.MATERIAL,
            'equipment': ResourceType.EQUIPMENT,
            'labor': ResourceType.LABOR,
            'human': ResourceType.LABOR
        }
        return type_map.get(
            str(resource_type).lower().strip(), ResourceType.MATERIAL
        )
    
    def _parse_resource_status(self, status: str) -> ResourceStatus:
        if pd.isna(status):
            return ResourceStatus.AVAILABLE
        
        status_map = {
            'available': ResourceStatus.AVAILABLE,
            'in_use': ResourceStatus.IN_USE,
            'active': ResourceStatus.IN_USE,
            'depleted': ResourceStatus.DEPLETED,
            'maintenance': ResourceStatus.MAINTENANCE,
            'ordered': ResourceStatus.AVAILABLE,
            'retired': ResourceStatus.DEPLETED
        }
        return status_map.get(
            str(status).lower().strip(), ResourceStatus.AVAILABLE
        )