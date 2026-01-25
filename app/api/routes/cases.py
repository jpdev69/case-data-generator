from typing import List
import io

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse, StreamingResponse

from app.data.sample_cases import SAMPLE_CASES, get_case_by_id
from app.schemas.cases import Case, ObjectiveSpec
from app.services.case_generator import (
    generate_random_case,
    generate_data_analysis_case,
    _generate_financial_case,
    _generate_financial_objectives,
    _generate_data_analysis_objectives,
    _generate_financial_objectives_contextual,
    _generate_data_analysis_objectives_contextual,
    calculate_case_generation_capacity,
)
from app.services.mock_data_generator import generate_mock_data, format_mock_data_summary
from app.services.excel_generator import generate_excel_from_mock_data

router = APIRouter(prefix="/cases", tags=["cases"])


@router.get("/", response_model=List[Case], summary="List available cases")
async def list_cases() -> List[Case]:
    return SAMPLE_CASES


@router.get("/{case_id}", response_model=Case, summary="Get a case by id")
async def get_case(case_id: str) -> Case:
    case = get_case_by_id(case_id)
    if case:
        return case
    raise HTTPException(status_code=404, detail="Case not found")


@router.get("/info/capacity", summary="Get case generation capacity information")
async def get_capacity_info() -> dict:
    """Get information about the total number of unique cases that can be generated."""
    return calculate_case_generation_capacity()


@router.post("/generate", response_model=Case, summary="Generate a random practice case")
async def generate_case() -> Case:
    """Generate a random practice case - either financial VA or data analysis (50/50)."""

    return generate_random_case()


@router.post("/generate/financial", response_model=Case, summary="Generate a financial VA practice case")
async def generate_financial_case_endpoint() -> Case:
    """Generate a unique, realistic financial VA practice case."""

    return _generate_financial_case()


@router.post("/generate/data-analysis", response_model=Case, summary="Generate a data analysis practice case")
async def generate_data_analysis_case_endpoint() -> Case:
    """Generate a unique data analysis case focused on identifying business problems and bottlenecks."""

    return generate_data_analysis_case()


@router.post("/{case_id}/generate-objectives", response_model=list[ObjectiveSpec], summary="Generate additional objectives for a case")
async def generate_case_objectives(case_id: str) -> list[ObjectiveSpec]:
    """Generate detailed objectives for an existing case based on its context, deliverables, and tools."""
    
    # Try to find in sample cases first
    case = get_case_by_id(case_id)
    
    # If not found in sample cases, we need to regenerate or return error
    # For now, return a generic set based on case_id pattern
    if not case:
        # Case was dynamically generated and not persisted, return appropriate objectives
        # We'll determine type from the case_id pattern
        if "problem" in case_id.lower() or "analysis" in case_id.lower():
            return _generate_data_analysis_objectives()
        else:
            return _generate_financial_objectives()
    
    # Prefer explicit case_type if present, otherwise fall back to keyword detection
    if getattr(case, "case_type", "financial") == "analysis":
        return _generate_data_analysis_objectives_contextual(case)
    elif getattr(case, "case_type", "financial") == "financial":
        return _generate_financial_objectives_contextual(case)
    else:
        # Fallback to keywords if unknown type
        context_lower = case.context.lower()
        financial_keywords = ["needs", "financial", "analysis", "budget", "cash flow", "revenue", "expense", "payroll", "reconciliation"]
        is_financial_case = any(keyword in context_lower for keyword in financial_keywords) and "problem" not in context_lower
        return _generate_financial_objectives_contextual(case) if is_financial_case else _generate_data_analysis_objectives_contextual(case)


@router.post("/mock-data/generate", summary="Generate mock data for a case")
async def generate_case_mock_data(case: Case) -> dict:
    """Generate realistic mock data based on the case type and deliverables."""
    
    mock_data = generate_mock_data(case)
    summary = format_mock_data_summary(mock_data)
    
    return {
        "success": True,
        "summary": summary,
        "data": mock_data
    }


@router.post("/mock-data/download", summary="Download mock data as Excel")
async def download_mock_data_excel(case: Case) -> StreamingResponse:
    """Generate and download mock data as an Excel file."""
    
    mock_data = generate_mock_data(case)
    excel_bytes = generate_excel_from_mock_data(case, mock_data)
    
    # Create filename
    filename = f"mock_data_{case.id}.xlsx"
    
    stream = io.BytesIO(excel_bytes)
    stream.seek(0)

    return StreamingResponse(
        stream,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={
            "Content-Disposition": f"attachment; filename={filename}",
            "Content-Length": str(len(excel_bytes)),
            "Access-Control-Expose-Headers": "Content-Disposition"
        }
    )

@router.post("/objectives/generate", response_model=list[ObjectiveSpec], summary="Generate contextual objectives for a case")
async def generate_case_objectives_from_case(case: Case) -> list[ObjectiveSpec]:
    """Generate detailed objectives based on full case data including context, deliverables, and tools."""
    
    # Prefer explicit case_type if present, otherwise fall back to keyword detection
    if getattr(case, "case_type", "financial") == "analysis":
        return _generate_data_analysis_objectives_contextual(case)
    elif getattr(case, "case_type", "financial") == "financial":
        return _generate_financial_objectives_contextual(case)
    else:
        # Fallback to keywords if unknown type
        context_lower = case.context.lower()
        financial_keywords = ["needs", "financial", "analysis", "budget", "cash flow", "revenue", "expense", "payroll", "reconciliation"]
        is_financial_case = any(keyword in context_lower for keyword in financial_keywords) and "problem" not in context_lower
        return _generate_financial_objectives_contextual(case) if is_financial_case else _generate_data_analysis_objectives_contextual(case)
