from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from app.database import Base


class TaskStatus(str, enum.Enum):
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    DELAYED = "delayed"
    BLOCKED = "blocked"


class TaskPriority(str, enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class Task(Base):
    __tablename__ = "tasks"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    
    name = Column(String(255), nullable=False)
    description = Column(Text)
    status = Column(Enum(TaskStatus), default=TaskStatus.NOT_STARTED)
    priority = Column(Enum(TaskPriority), default=TaskPriority.MEDIUM)
    
    # Dates
    start_date = Column(DateTime)
    planned_end_date = Column(DateTime)
    actual_end_date = Column(DateTime, nullable=True)
    
    # Progress
    progress_percentage = Column(Float, default=0.0)
    
    # Assignment
    assigned_to = Column(String(255))
    
    # Dependencies
    depends_on_task_id = Column(Integer, ForeignKey("tasks.id"), nullable=True)
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    project = relationship("Project", back_populates="tasks")
    dependencies = relationship("Task", remote_side=[id])
    
    @property
    def is_overdue(self):
        """Check if task is overdue"""
        if self.status != TaskStatus.COMPLETED and self.planned_end_date:
            return datetime.utcnow() > self.planned_end_date
        return False