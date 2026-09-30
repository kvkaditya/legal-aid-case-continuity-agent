"""
Case API routes
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.case import (
    CaseSchema,
    CaseListSchema,
    HearingSchema,
    CommitmentSchema,
    PendingItemSchema,
    DocumentSchema,
)
from app.services.case import CaseService

router = APIRouter(prefix="/api/cases", tags=["cases"])


@router.get("/", response_model=list[CaseListSchema])
async def list_cases(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    """Get all cases"""
    cases = CaseService.get_all_cases(db, skip=skip, limit=limit)
    return cases


@router.get("/{case_id}", response_model=CaseSchema)
async def get_case(
    case_id: int,
    db: Session = Depends(get_db),
):
    """Get a specific case with all details"""
    case = CaseService.get_case(db, case_id)
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
    return case


@router.get("/{case_id}/hearings", response_model=list[HearingSchema])
async def get_case_hearings(
    case_id: int,
    db: Session = Depends(get_db),
):
    """Get all hearings for a case"""
    case = CaseService.get_case(db, case_id)
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
    return case.hearings


@router.get("/{case_id}/commitments", response_model=list[CommitmentSchema])
async def get_case_commitments(
    case_id: int,
    db: Session = Depends(get_db),
):
    """Get all commitments for a case"""
    case = CaseService.get_case(db, case_id)
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
    return case.commitments


@router.get("/{case_id}/pending-items", response_model=list[PendingItemSchema])
async def get_case_pending_items(
    case_id: int,
    db: Session = Depends(get_db),
):
    """Get all pending items for a case"""
    case = CaseService.get_case(db, case_id)
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
    return case.pending_items


@router.get("/{case_id}/documents", response_model=list[DocumentSchema])
async def get_case_documents(
    case_id: int,
    db: Session = Depends(get_db),
):
    """Get all documents for a case"""
    case = CaseService.get_case(db, case_id)
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
    return case.documents


@router.get("/{case_id}/hearings/{hearing_id}", response_model=HearingSchema)
async def get_hearing_details(
    case_id: int,
    hearing_id: int,
    db: Session = Depends(get_db),
):
    """Get detailed information about a specific hearing"""
    case = CaseService.get_case(db, case_id)
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
    
    hearing = CaseService.get_hearing(db, hearing_id)
    if not hearing or hearing.case_id != case_id:
        raise HTTPException(status_code=404, detail="Hearing not found")
    
    return hearing


@router.get("/{case_id}/unfulfilled-commitments", response_model=list[CommitmentSchema])
async def get_unfulfilled_commitments(
    case_id: int,
    db: Session = Depends(get_db),
):
    """Get all unfulfilled commitments for a case"""
    case = CaseService.get_case(db, case_id)
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
    
    commitments = CaseService.get_unfulfilled_commitments(db, case_id)
    return commitments


@router.get("/{case_id}/pending-items-by-status", response_model=list[PendingItemSchema])
async def get_pending_items_by_status(
    case_id: int,
    status: str = "pending",
    db: Session = Depends(get_db),
):
    """Get pending items by status"""
    case = CaseService.get_case(db, case_id)
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
    
    pending_items = [item for item in case.pending_items if item.status == status]
    return pending_items
