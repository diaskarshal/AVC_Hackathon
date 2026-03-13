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
    source = Column(String(100))
    lot_number = Column(String(100))
    status = Column(Enum(TenderStatus), default=TenderStatus.UPLOADED)

    raw_text = Column(Text)

    parsed_scope = Column(JSON)

    # Embedding vector stored as JSON list (for similarity search)
    embedding = Column(JSON)

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

    plan_data = Column(JSON)

    estimated_total_cost = Column(Float, default=0.0)
    estimated_duration_days = Column(Integer)

    similar_project_ids = Column(JSON)
    confidence_score = Column(Float)

    llm_reasoning = Column(Text)

    created_at = Column(DateTime, default=datetime.utcnow)

    tender = relationship("Tender", back_populates="resource_plans")