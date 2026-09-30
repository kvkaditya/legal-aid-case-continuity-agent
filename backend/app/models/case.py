"""
Database models for Case Management
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum, Boolean
from sqlalchemy.orm import relationship
from app.database import Base
import enum


class CaseStatus(str, enum.Enum):
    """Case status enumeration"""
    ONGOING = "ongoing"
    CLOSED = "closed"
    PENDING = "pending"
    SUSPENDED = "suspended"


class HearingStatus(str, enum.Enum):
    """Hearing status enumeration"""
    SCHEDULED = "scheduled"
    COMPLETED = "completed"
    ADJOURNED = "adjourned"
    POSTPONED = "postponed"


class Case(Base):
    """Case model"""
    __tablename__ = "cases"

    id = Column(Integer, primary_key=True, index=True)
    case_number = Column(String(50), unique=True, index=True, nullable=False)
    title = Column(String(255), nullable=False)
    petitioner = Column(String(255), nullable=False)
    respondent = Column(String(255), nullable=False)
    description = Column(Text)
    status = Column(Enum(CaseStatus), default=CaseStatus.ONGOING, nullable=False)
    filing_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    court_name = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    hearings = relationship("Hearing", back_populates="case", cascade="all, delete-orphan")
    documents = relationship("Document", back_populates="case", cascade="all, delete-orphan")
    commitments = relationship("Commitment", back_populates="case", cascade="all, delete-orphan")
    pending_items = relationship("PendingItem", back_populates="case", cascade="all, delete-orphan")


class Hearing(Base):
    """Hearing model"""
    __tablename__ = "hearings"

    id = Column(Integer, primary_key=True, index=True)
    case_id = Column(Integer, ForeignKey("cases.id", ondelete="CASCADE"), nullable=False)
    hearing_number = Column(Integer, nullable=False)
    hearing_date = Column(DateTime, nullable=False)
    description = Column(Text)
    status = Column(Enum(HearingStatus), default=HearingStatus.SCHEDULED, nullable=False)
    judge_name = Column(String(255))
    location = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    case = relationship("Case", back_populates="hearings")
    court_directions = relationship("CourtDirection", back_populates="hearing", cascade="all, delete-orphan")
    commitments = relationship("Commitment", back_populates="hearing", cascade="all, delete-orphan")


class Document(Base):
    """Document model"""
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    case_id = Column(Integer, ForeignKey("cases.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    document_type = Column(String(100), nullable=False)
    file_path = Column(String(500))
    uploaded_date = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    case = relationship("Case", back_populates="documents")


class CourtDirection(Base):
    """Court Direction model"""
    __tablename__ = "court_directions"

    id = Column(Integer, primary_key=True, index=True)
    hearing_id = Column(Integer, ForeignKey("hearings.id", ondelete="CASCADE"), nullable=False)
    direction_text = Column(Text, nullable=False)
    directed_to = Column(String(255), nullable=False)
    direction_date = Column(DateTime, default=datetime.utcnow)
    expected_completion_date = Column(DateTime)
    is_resolved = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    hearing = relationship("Hearing", back_populates="court_directions")


class Commitment(Base):
    """Commitment model (lawyer/party commitment to do something)"""
    __tablename__ = "commitments"

    id = Column(Integer, primary_key=True, index=True)
    case_id = Column(Integer, ForeignKey("cases.id", ondelete="CASCADE"), nullable=False)
    hearing_id = Column(Integer, ForeignKey("hearings.id", ondelete="CASCADE"), nullable=False)
    committed_by = Column(String(255), nullable=False)  # Name of party making commitment
    commitment_text = Column(Text, nullable=False)
    commitment_date = Column(DateTime, default=datetime.utcnow)
    expected_completion_date = Column(DateTime)
    is_fulfilled = Column(Boolean, default=False)
    fulfillment_date = Column(DateTime)
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    case = relationship("Case", back_populates="commitments")
    hearing = relationship("Hearing", back_populates="commitments")


class PendingItem(Base):
    """Pending Item model (tasks/items pending resolution)"""
    __tablename__ = "pending_items"

    id = Column(Integer, primary_key=True, index=True)
    case_id = Column(Integer, ForeignKey("cases.id", ondelete="CASCADE"), nullable=False)
    hearing_id = Column(Integer, ForeignKey("hearings.id", ondelete="CASCADE"), nullable=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    item_type = Column(String(100), nullable=False)  # e.g., "payment", "document", "submission"
    status = Column(String(50), default="pending", nullable=False)  # pending, in_progress, resolved
    raised_date = Column(DateTime, default=datetime.utcnow)
    expected_resolution_date = Column(DateTime)
    resolved_date = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    case = relationship("Case", back_populates="pending_items")
