from enum import Enum
from typing import List
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class SubmissionStatus(str, Enum):
    pending = "pending"
    validating = "validating"
    rejected = "rejected"
    accepted = "accepted"


class SubmissionFile(BaseModel):
    deliverable_name: str = Field(..., description="Name matching a deliverable spec")
    file_name: str = Field(..., description="Uploaded file name including extension")


class SubmissionCreateRequest(BaseModel):
    case_id: str
    files: List[SubmissionFile] = Field(..., min_items=1)


class SubmissionResponse(BaseModel):
    submission_id: UUID = Field(default_factory=uuid4)
    status: SubmissionStatus = Field(default=SubmissionStatus.validating)
    case_id: str
    issues: List[str] = Field(default_factory=list, description="Validation issues, if any")
