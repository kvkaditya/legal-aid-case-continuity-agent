"""
Database seed data
"""
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.models.case import Case, Hearing, Document, CourtDirection, Commitment, PendingItem
from app.models.case import CaseStatus, HearingStatus


def seed_demo_data(db: Session) -> None:
    """
    Create demo case data for Ramesh Kumar vs State Housing Authority
    """
    # Check if case already exists
    existing_case = db.query(Case).filter(Case.case_number == "CASE-2023-001").first()
    if existing_case:
        return

    # Create the main case
    case = Case(
        case_number="CASE-2023-001",
        title="Ramesh Kumar vs State Housing Authority",
        petitioner="Ramesh Kumar",
        respondent="State Housing Authority",
        description="A case regarding housing allocation and compensation for wrongful denial of housing benefits",
        status=CaseStatus.ONGOING,
        filing_date=datetime(2023, 6, 15),
        court_name="High Court of [State] - Housing Division",
    )
    db.add(case)
    db.flush()

    # Create 7 hearings
    base_date = datetime(2023, 7, 1)

    # Hearing 1
    hearing_1 = Hearing(
        case_id=case.id,
        hearing_number=1,
        hearing_date=base_date,
        description="First hearing - Initial arguments by both parties",
        status=HearingStatus.COMPLETED,
        judge_name="Hon. Justice Sharma",
        location="Court Room 3, High Court",
    )
    db.add(hearing_1)
    db.flush()

    # Hearing 2
    hearing_2 = Hearing(
        case_id=case.id,
        hearing_number=2,
        hearing_date=base_date + timedelta(days=30),
        description="Second hearing - Submission of preliminary documents",
        status=HearingStatus.COMPLETED,
        judge_name="Hon. Justice Sharma",
        location="Court Room 3, High Court",
    )
    db.add(hearing_2)
    db.flush()

    # Hearing 3 - Important: Court directs payment statement
    hearing_3 = Hearing(
        case_id=case.id,
        hearing_number=3,
        hearing_date=base_date + timedelta(days=60),
        description="Third hearing - Discussion on financial statements",
        status=HearingStatus.COMPLETED,
        judge_name="Hon. Justice Sharma",
        location="Court Room 3, High Court",
    )
    db.add(hearing_3)
    db.flush()

    # Court direction in Hearing 3
    court_direction_3 = CourtDirection(
        hearing_id=hearing_3.id,
        direction_text="Respondent to submit comprehensive payment statement for all housing benefit transactions",
        directed_to="State Housing Authority",
        direction_date=hearing_3.hearing_date,
        expected_completion_date=hearing_3.hearing_date + timedelta(days=14),
        is_resolved=False,
    )
    db.add(court_direction_3)

    # Commitment in Hearing 3
    commitment_3 = Commitment(
        case_id=case.id,
        hearing_id=hearing_3.id,
        committed_by="Petitioner's Lawyer",
        commitment_text="Will submit bank statement showing denial of benefits",
        commitment_date=hearing_3.hearing_date,
        expected_completion_date=hearing_3.hearing_date + timedelta(days=14),
        is_fulfilled=False,
    )
    db.add(commitment_3)

    # Pending item for Hearing 3
    pending_3 = PendingItem(
        case_id=case.id,
        hearing_id=hearing_3.id,
        title="Payment Statement Submission",
        description="Payment statement from respondent - Status: Still pending",
        item_type="payment",
        status="pending",
        raised_date=hearing_3.hearing_date,
        expected_resolution_date=hearing_3.hearing_date + timedelta(days=14),
    )
    db.add(pending_3)
    db.flush()

    # Hearing 4 - Bank statement submitted
    hearing_4 = Hearing(
        case_id=case.id,
        hearing_number=4,
        hearing_date=base_date + timedelta(days=90),
        description="Fourth hearing - Bank statement submission",
        status=HearingStatus.COMPLETED,
        judge_name="Hon. Justice Sharma",
        location="Court Room 3, High Court",
    )
    db.add(hearing_4)
    db.flush()

    # Document submitted in Hearing 4
    doc_4 = Document(
        case_id=case.id,
        title="Bank Statement",
        description="Bank statement showing denial of housing benefits",
        document_type="bank_statement",
        uploaded_date=hearing_4.hearing_date,
    )
    db.add(doc_4)

    # Commitment fulfilled in Hearing 4
    commitment_4 = Commitment(
        case_id=case.id,
        hearing_id=hearing_4.id,
        committed_by="Petitioner's Lawyer",
        commitment_text="Bank statement submitted and filed with court",
        commitment_date=hearing_4.hearing_date,
        is_fulfilled=True,
        fulfillment_date=hearing_4.hearing_date,
    )
    db.add(commitment_4)

    # Update Hearing 3's pending item
    pending_3.status = "in_progress"
    db.flush()

    # Hearing 5 - Payment statement not found
    hearing_5 = Hearing(
        case_id=case.id,
        hearing_number=5,
        hearing_date=base_date + timedelta(days=120),
        description="Fifth hearing - Respondent's payment statement status",
        status=HearingStatus.COMPLETED,
        judge_name="Hon. Justice Sharma",
        location="Court Room 3, High Court",
    )
    db.add(hearing_5)
    db.flush()

    # Pending item for Hearing 5
    pending_5 = PendingItem(
        case_id=case.id,
        hearing_id=hearing_5.id,
        title="Payment Statement Not Found",
        description="Payment statement is not found in available case records - Respondent's failure to comply",
        item_type="payment",
        status="pending",
        raised_date=hearing_5.hearing_date,
    )
    db.add(pending_5)

    # Court direction in Hearing 5
    court_direction_5 = CourtDirection(
        hearing_id=hearing_5.id,
        direction_text="Respondent must provide certified payment records or explain non-compliance",
        directed_to="State Housing Authority",
        direction_date=hearing_5.hearing_date,
        expected_completion_date=hearing_5.hearing_date + timedelta(days=21),
        is_resolved=False,
    )
    db.add(court_direction_5)
    db.flush()

    # Hearing 6 - Payment statement remains unresolved
    hearing_6 = Hearing(
        case_id=case.id,
        hearing_number=6,
        hearing_date=base_date + timedelta(days=150),
        description="Sixth hearing - Review of outstanding payment statement issue",
        status=HearingStatus.COMPLETED,
        judge_name="Hon. Justice Sharma",
        location="Court Room 3, High Court",
    )
    db.add(hearing_6)
    db.flush()

    # Pending item for Hearing 6
    pending_6 = PendingItem(
        case_id=case.id,
        hearing_id=hearing_6.id,
        title="Payment Statement Remains Unresolved",
        description="Payment statement issue continues to remain unresolved despite court directions",
        item_type="payment",
        status="pending",
        raised_date=hearing_6.hearing_date,
    )
    db.add(pending_6)

    # Court direction in Hearing 6
    court_direction_6 = CourtDirection(
        hearing_id=hearing_6.id,
        direction_text="Matter to be listed for further hearing; respondent's compliance to be reviewed",
        directed_to="State Housing Authority",
        direction_date=hearing_6.hearing_date,
        is_resolved=False,
    )
    db.add(court_direction_6)
    db.flush()

    # Hearing 7 - Upcoming hearing
    hearing_7 = Hearing(
        case_id=case.id,
        hearing_number=7,
        hearing_date=base_date + timedelta(days=180),
        description="Seventh hearing - Final arguments and judgment preparation",
        status=HearingStatus.SCHEDULED,
        judge_name="Hon. Justice Sharma",
        location="Court Room 3, High Court",
    )
    db.add(hearing_7)
    db.flush()

    # Pending item for Hearing 7
    pending_7 = PendingItem(
        case_id=case.id,
        hearing_id=hearing_7.id,
        title="Upcoming Hearing",
        description="Final hearing scheduled for case resolution",
        item_type="hearing",
        status="pending",
        raised_date=datetime.utcnow(),
        expected_resolution_date=hearing_7.hearing_date,
    )
    db.add(pending_7)

    db.commit()
