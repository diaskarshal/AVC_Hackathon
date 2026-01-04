from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class Budget(Base):
    __tablename__ = "budgets"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    
    category = Column(String(255), nullable=False)
    description = Column(Text)
    
    planned_amount = Column(Float, default=0.0)
    actual_amount = Column(Float, default=0.0)
    
    budget_date = Column(DateTime, default=datetime.utcnow)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    project = relationship("Project", back_populates="budgets")
    
    @property
    def variance(self):
        return self.planned_amount - self.actual_amount
    
    @property
    def variance_percentage(self):
        if self.planned_amount == 0:
            return 0
        return (self.variance / self.planned_amount) * 100