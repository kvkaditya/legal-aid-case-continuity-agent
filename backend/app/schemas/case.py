"""
Pydantic schemas for Case Management
"""
from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional, List


class CourtDirectionSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    hearing_id: int
    direction_text: str
    directed_to: str
    direction_date: datetime
    expected_completion_date: Optional[datetime] = None
    is_resolved: bool


class CommitmentSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    case_id: int
    hearing_id: int
    committed_by: str
    commitment_text: str
    commitment_date: datetime
    expected_completion_date: Optional[datetime] = None
    is_fulfilled: bool
    fulfillment_date: Optional[datetime] = None
    notes: Optional[str] = None


class DocumentSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    case_id: int
    title: str
    description: Optional[str] = None
    document_type: str
    file_path: Optional[str] = None
    uploaded_date: datetime


class PendingItemSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    case_id: int
    hearing_id: Optional[int] = None
    title: str
    description: Optional[str] = None
    item_type: str
    status: str
    raised_date: datetime
    expected_resolution_date: Optional[datetime] = None
    resolved_date: Optional[datetime] = None


class HearingSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    case_id: int
    hearing_number: int
    hearing_date: datetime
    description: Optional[str] = None
    status: str
    judge_name: Optional[str] = None
    location: Optional[str] = None
    court_directions: List[CourtDirectionSchema] = []
    commitments: List[CommitmentSchema] = []


class CaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    case_number: str
    title: str
    petitioner: str
    respondent: str
    description: Optional[str] = None
    status: str
    filing_date: datetime
    court_name: str
    hearings: List[HearingSchema] = []
    documents: List[DocumentSchema] = []
    commitments: List[CommitmentSchema] = []
    pending_items: List[PendingItemSchema] = []


class CaseListSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    case_number: str
    title: str
    petitioner: str
    respondent: str
    status: str
    filing_date: datetime
    court_name: str

