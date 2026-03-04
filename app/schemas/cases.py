from typing import Dict, List, Optional

from pydantic import BaseModel, Field


class SheetRule(BaseModel):
    """Rules describing expected sheets and columns for a deliverable."""

    name: str = Field(..., description="Sheet/tab name")
    required_columns: List[str] = Field(default_factory=list)


class ObjectiveSpec(BaseModel):
    """Specific objective or milestone that must be achieved."""

    title: str = Field(..., description="Short title of the objective")
    description: str = Field(..., description="Detailed description of what needs to be achieved")
    success_criteria: List[str] = Field(default_factory=list, description="Measurable criteria for success")


class DeliverableSpec(BaseModel):
    name: str
    description: str
    file_types: List[str] = Field(..., description="Allowed file extensions, e.g. ['.xlsx', '.csv']")
    required_count: int = Field(default=1, ge=1)
    naming_rule: Optional[str] = Field(default=None, description="Naming convention the upload must follow")
    sheets: List[SheetRule] = Field(default_factory=list)
    calc_rules: List[str] = Field(default_factory=list, description="Human-readable calculation or logic expectations")


class BusinessContext(BaseModel):
    """Structured business context to shape case generation and mock data."""

    industry: Optional[str] = Field(default=None, description="Industry or vertical, e.g., 'SaaS startup', 'E-commerce'.")
    company_size: Optional[str] = Field(default=None, description="Company size, e.g., 'seed', 'SMB', 'mid-market', 'enterprise'.")
    region: Optional[str] = Field(default=None, description="Primary geography or market region.")
    goals: List[str] = Field(default_factory=list, description="Top business goals driving the analysis.")
    constraints: List[str] = Field(default_factory=list, description="Operational or regulatory constraints that affect data or outcomes.")
    kpis: List[str] = Field(default_factory=list, description="Key metrics of interest (e.g., MRR, churn rate, CAC, AR aging).")
    data_sources: List[str] = Field(default_factory=list, description="Systems to pull data from (e.g., QuickBooks, HubSpot, Stripe, Snowflake).")
    time_horizon: Optional[str] = Field(default=None, description="Time window like 'month', 'quarter', 'year', or explicit range.")
    problem_statement: Optional[str] = Field(default=None, description="Primary business problem to address, phrased succinctly.")
    notes: Optional[str] = Field(default=None, description="Additional freeform context or assumptions.")


class Case(BaseModel):
    id: str
    version: str = Field(default="v1")
    title: str
    context: str
    role: str
    case_type: str = Field(default="financial", description="Type of case: 'financial' or 'analysis'")
    data_profile: Optional[str] = Field(
        default=None,
        description=(
            "Explicit data-generation profile that determines which mock-data "
            "generator to use (e.g. 'cashflow', 'expense_audit', 'revenue_forecast', "
            "'payroll', 'customer_analytics', 'ops_sla', etc.). "
            "When set, the mock-data generator dispatches on this value instead of "
            "brittle keyword matching, guaranteeing the dataset matches the case scenario."
        ),
    )
    tools: List[str] = Field(default_factory=list)
    deadline_hours: int = Field(default=72, ge=1)
    urgency: str = Field(default="normal")
    deliverables: List[DeliverableSpec] = Field(default_factory=list)
    objectives: List[ObjectiveSpec] = Field(default_factory=list, description="Specific objectives to achieve")
    rubric: Dict[str, int] = Field(default_factory=dict, description="Score weights by rubric dimension")
    business_context: Optional[BusinessContext] = Field(default=None, description="Optional structured business context to inform generation.")
