from sqlalchemy import Column, Integer, String, Float, DateTime, Text, ForeignKey, JSON, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from app.database import Base


class TenderStatus(str, enum.Enum):
    UPLOADED = "uploaded"
    PARSED = "parsed"
    PLAN_GENERATED = "plan_generated"
    ACCEPTED = "accepted"


class Tender(Base):
    __tablename__ = "tenders"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(500), nullable=False)
    source = Column(String(100)) #goszakup, samruk, other
    lot_number = Column(String(100))
    status = Column(Enum(TenderStatus), default=TenderStatus.UPLOADED)

    # Raw extracted text from document
    raw_text = Column(Text)

    # Structured data extracted by LLM (stored as JSON)
    parsed_scope = Column(JSON)            # {work_type, equipment, location, volume, deadline_days}

    # Embedding vector stored as JSON list (for similarity search)
    embedding = Column(JSON)               # list of 384 floats

    # Reference to the project created from this tender (if accepted)
    created_project_id = Column(Integer, ForeignKey("projects.id"), nullable=True)

    file_name = Column(String(255))
    uploaded_by = Column(String(100))

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    resource_plans = relationship("TenderResourcePlan", back_populates="tender", cascade="all, delete-orphan")


class TenderResourcePlan(Base):
    __tablename__ = "tender_resource_plans"

    id = Column(Integer, primary_key=True, index=True)
    tender_id = Column(Integer, ForeignKey("tenders.id"), nullable=False)

    # The full plan as JSON — list of resource items
    plan_data = Column(JSON)
    # [{
    #   "resource_type": "labor|material|equipment",
    #   "name": "Сварщик 5 разряда",
    #   "quantity": 4,
    #   "unit": "чел/дн",
    #   "unit_cost": 15000,
    #   "total_cost": 60000,
    #   "notes": "На основе проекта ANPZ-2023"
    # }]

    estimated_total_cost = Column(Float, default=0.0)
    estimated_duration_days = Column(Integer)

    # Which historical project(s) were used as reference
    similar_project_ids = Column(JSON)     # [1, 3, 5]
    confidence_score = Column(Float)       # 0.0 - 1.0

    llm_reasoning = Column(Text)           # LLM's explanation of the estimate

    created_at = Column(DateTime, default=datetime.utcnow)

    tender = relationship("Tender", back_populates="resource_plans")