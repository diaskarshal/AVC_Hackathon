from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from app.database import Base


class ResourceType(str, enum.Enum):
    MATERIAL = "material"
    EQUIPMENT = "equipment"
    LABOR = "labor"


class ResourceStatus(str, enum.Enum):
    AVAILABLE = "available"
    IN_USE = "in_use"
    DEPLETED = "depleted"
    MAINTENANCE = "maintenance"


class Resource(Base):
    __tablename__ = "resources"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    
    name = Column(String(255), nullable=False)
    resource_type = Column(Enum(ResourceType), nullable=False)
    status = Column(Enum(ResourceStatus), default=ResourceStatus.AVAILABLE)
    
    # Quantities
    quantity = Column(Float, default=0.0)
    unit = Column(String(50))  # kg, m3, hours, pieces, etc.
    
    # Cost
    unit_cost = Column(Float, default=0.0)
    total_cost = Column(Float, default=0.0)
    
    # Supplier/Provider
    supplier = Column(String(255))
    
    # Dates
    allocated_date = Column(DateTime, default=datetime.utcnow)
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    project = relationship("Project", back_populates="resources")
    
    def calculate_total_cost(self):
        """Calculate total cost based on quantity and unit cost"""
        self.total_cost = self.quantity * self.unit_cost
        return self.total_cost