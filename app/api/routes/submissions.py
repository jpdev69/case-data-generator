from uuid import uuid4

from fastapi import APIRouter, HTTPException, status

from app.data.sample_cases import get_case_by_id
from app.schemas.submissions import (
    SubmissionCreateRequest,
    SubmissionResponse,
    SubmissionStatus,
)
from app.services.validator import validate_submission

router = APIRouter(prefix="/submissions", tags=["submissions"])


@router.post("/", response_model=SubmissionResponse, status_code=status.HTTP_202_ACCEPTED)
async def submit_deliverables(payload: SubmissionCreateRequest) -> SubmissionResponse:
    case = get_case_by_id(payload.case_id)
    if not case:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Case not found")

    validation = validate_submission(case, payload.files)
    status_value = SubmissionStatus.accepted if validation.accepted else SubmissionStatus.rejected

    return SubmissionResponse(
        submission_id=uuid4(),
        status=status_value,
        case_id=payload.case_id,
        issues=validation.issues,
    )
