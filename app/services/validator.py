from pathlib import Path
from typing import List, Tuple

from app.schemas.cases import Case, DeliverableSpec
from app.schemas.submissions import SubmissionFile


class ValidationResult:
    def __init__(self, accepted: bool, issues: List[str]):
        self.accepted = accepted
        self.issues = issues


def _ext_allowed(file_name: str, spec: DeliverableSpec) -> bool:
    ext = Path(file_name).suffix.lower()
    return ext in {extn.lower() for extn in spec.file_types}


def validate_submission(case: Case, files: List[SubmissionFile]) -> ValidationResult:
    """Deterministic checks before LLM grading.

    - All files reference known deliverables
    - File extensions are allowed
    - Required counts are met
    """

    issues: List[str] = []
    deliverable_by_name = {d.name: d for d in case.deliverables}
    counts = {d.name: 0 for d in case.deliverables}

    for f in files:
        spec = deliverable_by_name.get(f.deliverable_name)
        if not spec:
            issues.append(f"Unknown deliverable: {f.deliverable_name}")
            continue
        counts[f.deliverable_name] += 1
        if not _ext_allowed(f.file_name, spec):
            issues.append(
                f"File '{f.file_name}' for '{f.deliverable_name}' must be one of {spec.file_types}"
            )

    # Check counts vs required
    for name, spec in deliverable_by_name.items():
        if counts[name] < spec.required_count:
            issues.append(
                f"Deliverable '{name}' requires {spec.required_count} file(s); received {counts[name]}"
            )

    return ValidationResult(accepted=len(issues) == 0, issues=issues)
