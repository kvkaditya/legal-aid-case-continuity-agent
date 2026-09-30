"""
Tests for database models
"""
import pytest
from datetime import datetime
from sqlalchemy.orm import Session
from app.models.case import Case, Hearing, Document, CourtDirection, Commitment, PendingItem
from app.models.case import CaseStatus, HearingStatus


def test_case_creation(db: Session):
    """Test creating a case"""
    case = Case(
        case_number="TEST-001",
        title="Test Case",
        petitioner="Test Petitioner",
        respondent="Test Respondent",
        court_name="Test Court",
        status=CaseStatus.ONGOING,
        filing_date=datetime.utcnow(),
    )
    db.add(case)
    db.commit()
    
    retrieved_case = db.query(Case).filter(Case.case_number == "TEST-001").first()
    assert retrieved_case is not None
    assert retrieved_case.title == "Test Case"


def test_hearing_belongs_to_case(db: Session):
    """Test hearing relationship with case"""
    case = db.query(Case).filter(Case.case_number == "CASE-2023-001").first()
    assert case is not None
    
    hearings = case.hearings
    assert len(hearings) == 7


def test_commitments_have_case_and_hearing(db: Session):
    """Test commitment relationships"""
    case = db.query(Case).filter(Case.case_number == "CASE-2023-001").first()
    commitments = case.commitments
    
    assert len(commitments) > 0
    for commitment in commitments:
        assert commitment.case_id == case.id
        assert commitment.hearing_id is not None


def test_court_directions_have_hearing(db: Session):
    """Test court direction relationships"""
    case = db.query(Case).filter(Case.case_number == "CASE-2023-001").first()
    hearing_3 = db.query(Hearing).filter(
        Hearing.case_id == case.id,
        Hearing.hearing_number == 3
    ).first()
    
    assert hearing_3 is not None
    assert len(hearing_3.court_directions) > 0


def test_pending_items_have_case(db: Session):
    """Test pending item relationships"""
    case = db.query(Case).filter(Case.case_number == "CASE-2023-001").first()
    pending_items = case.pending_items
    
    assert len(pending_items) > 0
    for item in pending_items:
        assert item.case_id == case.id


def test_documents_have_case(db: Session):
    """Test document relationships"""
    case = db.query(Case).filter(Case.case_number == "CASE-2023-001").first()
    documents = case.documents
    
    # Should have at least the bank statement document
    assert len(documents) > 0


def test_cascade_delete(db: Session):
    """Test cascade delete relationships"""
    case = db.query(Case).filter(Case.case_number == "CASE-2023-001").first()
    case_id = case.id
    
    # Delete the case
    db.delete(case)
    db.commit()
    
    # Check related objects are deleted
    deleted_case = db.query(Case).filter(Case.id == case_id).first()
    assert deleted_case is None
    
    hearings = db.query(Hearing).filter(Hearing.case_id == case_id).all()
    assert len(hearings) == 0


def test_hearing_status_enum(db: Session):
    """Test hearing status enumeration"""
    case = db.query(Case).filter(Case.case_number == "CASE-2023-001").first()
    
    completed_hearings = [h for h in case.hearings if h.status == HearingStatus.COMPLETED]
    scheduled_hearings = [h for h in case.hearings if h.status == HearingStatus.SCHEDULED]
    
    assert len(completed_hearings) > 0
    assert len(scheduled_hearings) > 0


def test_timestamps(db: Session):
    """Test timestamp fields"""
    case = db.query(Case).filter(Case.case_number == "CASE-2023-001").first()
    
    assert case.created_at is not None
    assert case.updated_at is not None
    assert case.filing_date is not None
