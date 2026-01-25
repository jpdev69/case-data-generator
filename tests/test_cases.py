from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_list_cases_returns_seed():
    resp = client.get("/api/cases")
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) >= 1
    assert any(c["id"] == "case-monthly-cashflow" for c in data)


def test_get_case_by_id():
    resp = client.get("/api/cases/case-monthly-cashflow")
    assert resp.status_code == 200
    data = resp.json()
    assert data["title"].startswith("Monthly Cash Flow")


def test_generate_case_returns_case():
    resp = client.post("/api/cases/generate")
    assert resp.status_code == 200
    data = resp.json()
    assert data["id"]
    assert data["deliverables"]
