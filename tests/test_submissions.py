from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


VALID_FILES = [
    {
        "deliverable_name": "Monthly Cash Flow Tracker",
        "file_name": "cashflow_acme_202501.xlsx",
    },
    {
        "deliverable_name": "Invoice and AR Detail",
        "file_name": "ar_aging_acme_20250101.xlsx",
    },
    {
        "deliverable_name": "CRM Segmentation Export",
        "file_name": "crm_segments_acme_20250101.csv",
    },
    {
        "deliverable_name": "Executive Summary",
        "file_name": "exec_summary_acme_20250101.pdf",
    },
]


def test_submit_valid_payload():
    resp = client.post(
        "/api/submissions",
        json={"case_id": "case-monthly-cashflow", "files": VALID_FILES},
    )
    assert resp.status_code == 202
    data = resp.json()
    assert data["status"] == "accepted"
    assert data["issues"] == []
    assert data["case_id"] == "case-monthly-cashflow"


def test_submit_unknown_case():
    resp = client.post(
        "/api/submissions",
        json={"case_id": "missing-case", "files": VALID_FILES},
    )
    assert resp.status_code == 404


def test_submit_bad_extension():
    payload = {
        "case_id": "case-monthly-cashflow",
        "files": [
            {
                "deliverable_name": "Monthly Cash Flow Tracker",
                "file_name": "cashflow_acme_202501.xls",  # wrong extension
            }
        ],
    }
    resp = client.post("/api/submissions", json=payload)
    assert resp.status_code == 202
    data = resp.json()
    assert data["status"] == "rejected"
    assert any("must be one of" in issue for issue in data["issues"])


def test_submit_missing_required_count():
    # Only CRM file supplied; other required deliverables missing
    payload = {
        "case_id": "case-monthly-cashflow",
        "files": [
            {
                "deliverable_name": "CRM Segmentation Export",
                "file_name": "crm_segments_acme_20250101.csv",
            }
        ],
    }
    resp = client.post("/api/submissions", json=payload)
    assert resp.status_code == 202
    data = resp.json()
    assert data["status"] == "rejected"
    assert any("requires" in issue for issue in data["issues"])
