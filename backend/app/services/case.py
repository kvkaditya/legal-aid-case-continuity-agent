"""
Case service for database operations
"""
from sqlalchemy.orm import Session
from app.models.case import Case, Hearing, Commitment, PendingItem, Document
from typing import List, Optional


class CaseService:
    """Service for case operations"""

    @staticmethod
    def get_case(db: Session, case_id: int) -> Optional[Case]:
        """Get a single case with all relationships"""
        return db.query(Case).filter(Case.id == case_id).first()

    @staticmethod
    def get_all_cases(db: Session, skip: int = 0, limit: int = 100) -> List[Case]:
        """Get all cases with pagination"""
        return db.query(Case).offset(skip).limit(limit).all()

    @staticmethod
    def get_case_by_number(db: Session, case_number: str) -> Optional[Case]:
        """Get case by case number"""
        return db.query(Case).filter(Case.case_number == case_number).first()

    @staticmethod
    def get_hearings_by_case(db: Session, case_id: int) -> List[Hearing]:
        """Get all hearings for a case"""
        return db.query(Hearing).filter(Hearing.case_id == case_id).order_by(Hearing.hearing_number).all()

    @staticmethod
    def get_hearing(db: Session, hearing_id: int) -> Optional[Hearing]:
        """Get a single hearing with relationships"""
        return db.query(Hearing).filter(Hearing.id == hearing_id).first()

    @staticmethod
    def get_commitments_by_case(db: Session, case_id: int) -> List[Commitment]:
        """Get all commitments for a case"""
        return db.query(Commitment).filter(Commitment.case_id == case_id).all()

    @staticmethod
    def get_commitments_by_hearing(db: Session, hearing_id: int) -> List[Commitment]:
        """Get all commitments for a hearing"""
        return db.query(Commitment).filter(Commitment.hearing_id == hearing_id).all()

    @staticmethod
    def get_pending_items_by_case(db: Session, case_id: int) -> List[PendingItem]:
        """Get all pending items for a case"""
        return db.query(PendingItem).filter(PendingItem.case_id == case_id).all()

    @staticmethod
    def get_pending_items_by_hearing(db: Session, hearing_id: int) -> List[PendingItem]:
        """Get all pending items for a hearing"""
        return db.query(PendingItem).filter(PendingItem.hearing_id == hearing_id).all()

    @staticmethod
    def get_documents_by_case(db: Session, case_id: int) -> List[Document]:
        """Get all documents for a case"""
        return db.query(Document).filter(Document.case_id == case_id).all()

    @staticmethod
    def get_pending_items_by_status(db: Session, status: str) -> List[PendingItem]:
        """Get pending items by status"""
        return db.query(PendingItem).filter(PendingItem.status == status).all()

    @staticmethod
    def get_unfulfilled_commitments(db: Session, case_id: int) -> List[Commitment]:
        """Get unfulfilled commitments for a case"""
        return db.query(Commitment).filter(
            Commitment.case_id == case_id,
            Commitment.is_fulfilled == False
        ).all()
