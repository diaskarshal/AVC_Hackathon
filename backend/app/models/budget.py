from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class Budget(Base):
    __tablename__ = "budgets"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    
    category = Column(String(255), nullable=False)  # Materials, Labor, Equipment, etc.
    description = Column(Text)
    
    # Financial
    planned_amount = Column(Float, default=0.0)
    actual_amount = Column(Float, default=0.0)
    
    # Dates
    budget_date = Column(DateTime, default=datetime.utcnow)
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    project = relationship("Project", back_populates="budgets")
    
    @property
    def variance(self):
        """Calculate budget variance (planned - actual)"""
        return self.planned_amount - self.actual_amount
    
    @property
    def variance_percentage(self):
        """Calculate variance as percentage"""
        if self.planned_amount == 0:
            return 0
        return (self.variance / self.planned_amount) * 100