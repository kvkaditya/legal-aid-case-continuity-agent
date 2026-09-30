"""
Tests for case endpoints
"""
import pytest
from fastapi.testclient import TestClient


def test_list_cases(client: TestClient):
    """Test listing all cases"""
    response = client.get("/api/cases/")
    assert response.status_code == 200
    cases = response.json()
    assert len(cases) > 0
    assert cases[0]["case_number"] == "CASE-2023-001"
    assert cases[0]["title"] == "Ramesh Kumar vs State Housing Authority"


def test_get_case_by_id(client: TestClient):
    """Test getting a specific case"""
    # First get all cases to find the ID
    response = client.get("/api/cases/")
    cases = response.json()
    case_id = cases[0]["id"]
    
    response = client.get(f"/api/cases/{case_id}")
    assert response.status_code == 200
    case = response.json()
    assert case["case_number"] == "CASE-2023-001"
    assert case["petitioner"] == "Ramesh Kumar"
    assert case["respondent"] == "State Housing Authority"
    assert len(case["hearings"]) == 7


def test_get_case_not_found(client: TestClient):
    """Test getting non-existent case"""
    response = client.get("/api/cases/9999")
    assert response.status_code == 404


def test_get_case_hearings(client: TestClient):
    """Test getting all hearings for a case"""
    response = client.get("/api/cases/")
    cases = response.json()
    case_id = cases[0]["id"]
    
    response = client.get(f"/api/cases/{case_id}/hearings")
    assert response.status_code == 200
    hearings = response.json()
    assert len(hearings) == 7
    
    # Check hearing numbers are in order
    for i, hearing in enumerate(hearings, 1):
        assert hearing["hearing_number"] == i


def test_get_hearing_details(client: TestClient):
    """Test getting details of a specific hearing"""
    response = client.get("/api/cases/")
    cases = response.json()
    case_id = cases[0]["id"]
    
    # Get hearings
    response = client.get(f"/api/cases/{case_id}/hearings")
    hearings = response.json()
    hearing_id = hearings[2]["id"]  # Hearing 3
    
    response = client.get(f"/api/cases/{case_id}/hearings/{hearing_id}")
    assert response.status_code == 200
    hearing = response.json()
    assert hearing["hearing_number"] == 3
    assert len(hearing["court_directions"]) > 0
    assert len(hearing["commitments"]) > 0


def test_get_case_commitments(client: TestClient):
    """Test getting all commitments for a case"""
    response = client.get("/api/cases/")
    cases = response.json()
    case_id = cases[0]["id"]
    
    response = client.get(f"/api/cases/{case_id}/commitments")
    assert response.status_code == 200
    commitments = response.json()
    assert len(commitments) >= 2  # At least 2 commitments from demo data


def test_get_case_pending_items(client: TestClient):
    """Test getting all pending items for a case"""
    response = client.get("/api/cases/")
    cases = response.json()
    case_id = cases[0]["id"]
    
    response = client.get(f"/api/cases/{case_id}/pending-items")
    assert response.status_code == 200
    pending_items = response.json()
    assert len(pending_items) >= 3


def test_get_case_documents(client: TestClient):
    """Test getting all documents for a case"""
    response = client.get("/api/cases/")
    cases = response.json()
    case_id = cases[0]["id"]
    
    response = client.get(f"/api/cases/{case_id}/documents")
    assert response.status_code == 200
    documents = response.json()
    # Should have at least the bank statement document
    assert any(doc["document_type"] == "bank_statement" for doc in documents)


def test_get_unfulfilled_commitments(client: TestClient):
    """Test getting unfulfilled commitments"""
    response = client.get("/api/cases/")
    cases = response.json()
    case_id = cases[0]["id"]
    
    response = client.get(f"/api/cases/{case_id}/unfulfilled-commitments")
    assert response.status_code == 200
    commitments = response.json()
    
    # All should be unfulfilled or fulfilled should be in separate list
    for commitment in commitments:
        assert commitment["is_fulfilled"] == False


def test_get_pending_items_by_status(client: TestClient):
    """Test filtering pending items by status"""
    response = client.get("/api/cases/")
    cases = response.json()
    case_id = cases[0]["id"]
    
    response = client.get(f"/api/cases/{case_id}/pending-items-by-status?status=pending")
    assert response.status_code == 200
    pending_items = response.json()
    
    # All should have status "pending"
    for item in pending_items:
        assert item["status"] == "pending"


def test_hearing_3_specifics(client: TestClient):
    """Test Hearing 3 specific requirements"""
    response = client.get("/api/cases/")
    cases = response.json()
    case_id = cases[0]["id"]
    
    response = client.get(f"/api/cases/{case_id}/hearings")
    hearings = response.json()
    hearing_3 = next((h for h in hearings if h["hearing_number"] == 3), None)
    
    assert hearing_3 is not None
    
    # Check court direction exists
    assert len(hearing_3["court_directions"]) > 0
    direction = hearing_3["court_directions"][0]
    assert "payment statement" in direction["direction_text"].lower()
    
    # Check commitment exists
    assert len(hearing_3["commitments"]) > 0
    commitment = hearing_3["commitments"][0]
    assert "bank statement" in commitment["commitment_text"].lower()


def test_hearing_4_document_submission(client: TestClient):
    """Test Hearing 4 - Bank statement submitted"""
    response = client.get("/api/cases/")
    cases = response.json()
    case_id = cases[0]["id"]
    
    response = client.get(f"/api/cases/{case_id}/documents")
    documents = response.json()
    
    # Should have bank statement
    bank_statements = [d for d in documents if d["document_type"] == "bank_statement"]
    assert len(bank_statements) > 0


def test_health_endpoint(client: TestClient):
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"


def test_root_endpoint(client: TestClient):
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "version" in data
