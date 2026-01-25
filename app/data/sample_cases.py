from typing import List, Optional

from app.schemas.cases import Case, DeliverableSpec, SheetRule


SAMPLE_CASES: List[Case] = [
    Case(
        id="case-monthly-cashflow",
        version="v1",
        title="Monthly Cash Flow and Receivables Hygiene",
        context=(
            "Boutique digital agency with lumpy retainers, needs clarity on runway and AR hygiene."
        ),
        role="Financial Support VA",
        case_type="financial",
        tools=["Excel", "HubSpot"],
        deadline_hours=72,
        urgency="high",
        deliverables=[
            DeliverableSpec(
                name="Monthly Cash Flow Tracker",
                description="12-week rolling cash flow with receipts vs disbursements",
                file_types=[".xlsx"],
                naming_rule="cashflow_<client>_<yyyymm>.xlsx",
                sheets=[
                    SheetRule(name="Summary", required_columns=["Week", "In", "Out", "Net", "Balance"]),
                    SheetRule(
                        name="Receipts",
                        required_columns=["Date", "Customer", "Amount", "Category", "Status"],
                    ),
                ],
                calc_rules=[
                    "Balance rolls forward from prior week",
                    "Net = In - Out",
                ],
            ),
            DeliverableSpec(
                name="Invoice and AR Detail",
                description="AR aging with invoice-level detail",
                file_types=[".xlsx"],
                naming_rule="ar_aging_<client>_<yyyymmdd>.xlsx",
                sheets=[
                    SheetRule(
                        name="Aging",
                        required_columns=["Customer", "Invoice", "Issued", "Due", "Amount", "Bucket"],
                    )
                ],
                calc_rules=["Aging bucket derived from due date"],
            ),
            DeliverableSpec(
                name="CRM Segmentation Export",
                description="Segmented open deals and customers",
                file_types=[".csv", ".xlsx"],
                naming_rule="crm_segments_<client>_<yyyymmdd>.csv",
                sheets=[],
                calc_rules=[],
            ),
            DeliverableSpec(
                name="Executive Summary",
                description="Narrative summary of risks and recommendations",
                file_types=[".pdf", ".docx"],
                naming_rule="exec_summary_<client>_<yyyymmdd>.pdf",
                sheets=[],
                calc_rules=[],
            ),
        ],
        rubric={
            "completeness": 25,
            "structure": 25,
            "financial_logic": 30,
            "communication": 20,
        },
    ),
    Case(
        id="case-expense-audit",
        version="v1",
        title="Quarterly Expense Audit and Budget Reconciliation",
        context=(
            "E-commerce startup preparing for Series A. Investors want clean expense categorization and budget variance analysis."
        ),
        role="Finance Operations Analyst",
        case_type="financial",
        tools=["Excel", "QuickBooks"],
        deadline_hours=48,
        urgency="urgent",
        deliverables=[
            DeliverableSpec(
                name="Expense Report by Category",
                description="Quarterly expenses broken down by department and category",
                file_types=[".xlsx"],
                naming_rule="expenses_q<quarter>_<yyyy>.xlsx",
                sheets=[
                    SheetRule(name="Summary", required_columns=["Department", "Category", "Budget", "Actual", "Variance"]),
                    SheetRule(name="Details", required_columns=["Date", "Vendor", "Amount", "Category", "Department"]),
                ],
                calc_rules=["Variance = Actual - Budget", "Variance % calculated"],
            ),
            DeliverableSpec(
                name="Budget vs Actual Dashboard",
                description="Visual comparison of planned vs actual spend",
                file_types=[".xlsx"],
                naming_rule="budget_dashboard_<yyyymmdd>.xlsx",
                sheets=[],
                calc_rules=[],
            ),
            DeliverableSpec(
                name="Findings Report",
                description="Written summary of anomalies and recommendations",
                file_types=[".pdf"],
                naming_rule="findings_<yyyymmdd>.pdf",
                sheets=[],
                calc_rules=[],
            ),
        ],
        rubric={
            "completeness": 30,
            "structure": 20,
            "financial_logic": 30,
            "communication": 20,
        },
    ),
    Case(
        id="case-revenue-forecast",
        version="v1",
        title="3-Month Revenue Forecast for SaaS Product",
        context=(
            "B2B SaaS company needs a rolling revenue forecast based on subscription tiers, churn rate, and new sign-ups."
        ),
        role="Revenue Analyst VA",
        case_type="financial",
        tools=["Excel", "Google Sheets"],
        deadline_hours=96,
        urgency="normal",
        deliverables=[
            DeliverableSpec(
                name="Revenue Forecast Model",
                description="Rolling 3-month forecast with MRR, churn, and expansion revenue",
                file_types=[".xlsx"],
                naming_rule="revenue_forecast_<yyyymm>.xlsx",
                sheets=[
                    SheetRule(name="Assumptions", required_columns=["Metric", "Value", "Source"]),
                    SheetRule(name="Forecast", required_columns=["Month", "New MRR", "Churn MRR", "Expansion MRR", "Total MRR"]),
                ],
                calc_rules=["Total MRR = Previous MRR + New - Churn + Expansion"],
            ),
            DeliverableSpec(
                name="Scenario Analysis",
                description="Best/worst/likely case scenarios",
                file_types=[".xlsx"],
                naming_rule="scenarios_<yyyymmdd>.xlsx",
                sheets=[],
                calc_rules=[],
            ),
            DeliverableSpec(
                name="Executive Brief",
                description="One-page summary with key insights",
                file_types=[".pdf", ".docx"],
                naming_rule="revenue_brief_<yyyymmdd>.pdf",
                sheets=[],
                calc_rules=[],
            ),
        ],
        rubric={
            "completeness": 25,
            "structure": 20,
            "financial_logic": 35,
            "communication": 20,
        },
    ),
    Case(
        id="case-payroll-reconciliation",
        version="v1",
        title="Monthly Payroll Reconciliation and Compliance Check",
        context=(
            "Growing consulting firm with contractors and full-time staff needs accurate payroll reconciliation and tax compliance verification."
        ),
        role="Payroll & Compliance VA",
        case_type="financial",
        tools=["Excel", "ADP", "Gusto"],
        deadline_hours=60,
        urgency="high",
        deliverables=[
            DeliverableSpec(
                name="Payroll Reconciliation Report",
                description="Month-end payroll totals reconciled against bank statements",
                file_types=[".xlsx"],
                naming_rule="payroll_recon_<yyyymm>.xlsx",
                sheets=[
                    SheetRule(name="Summary", required_columns=["Employee Type", "Gross Pay", "Deductions", "Net Pay", "Employer Taxes"]),
                    SheetRule(name="Details", required_columns=["Employee", "Gross", "Federal Tax", "State Tax", "Benefits", "Net"]),
                ],
                calc_rules=["Net Pay = Gross - Deductions", "Totals must match bank transfers"],
            ),
            DeliverableSpec(
                name="Tax Compliance Checklist",
                description="Verification that all tax withholdings are accurate",
                file_types=[".xlsx", ".pdf"],
                naming_rule="tax_compliance_<yyyymm>.xlsx",
                sheets=[],
                calc_rules=[],
            ),
            DeliverableSpec(
                name="Issue Log",
                description="Document any discrepancies or compliance risks",
                file_types=[".pdf", ".docx"],
                naming_rule="payroll_issues_<yyyymmdd>.pdf",
                sheets=[],
                calc_rules=[],
            ),
        ],
        rubric={
            "completeness": 30,
            "structure": 25,
            "financial_logic": 25,
            "communication": 20,
        },
    ),
    Case(
        id="case-customer-analytics",
        version="v1",
        title="Customer Behavior Analytics and Segmentation",
        context=(
            "E-commerce platform needs deep dive into customer segments, purchase patterns, and churn predictors for retention strategy."
        ),
        role="Data Analytics Consultant",
        case_type="analysis",
        tools=["Python", "SQL", "Tableau"],
        deadline_hours=96,
        urgency="high",
        deliverables=[
            DeliverableSpec(
                name="Customer Segmentation Report",
                description="Behavioral segments with metrics and profiles",
                file_types=[".xlsx", ".pdf"],
                naming_rule="customer_segments_<yyyymmdd>.xlsx",
                sheets=[],
                calc_rules=[],
            ),
            DeliverableSpec(
                name="Churn Analysis Dashboard",
                description="Identify high-risk segments and churn predictors",
                file_types=[".xlsx", ".pdf"],
                naming_rule="churn_analysis_<yyyymmdd>.xlsx",
                sheets=[],
                calc_rules=[],
            ),
        ],
        rubric={
            "completeness": 25,
            "insight_quality": 30,
            "methodology": 25,
            "communication": 20,
        },
    ),
    Case(
        id="case-performance-metrics",
        version="v1",
        title="Product Performance Metrics and Anomaly Detection",
        context=(
            "SaaS product experiencing unexpected performance dips. Need root cause analysis of user engagement drop and system anomalies."
        ),
        role="Product Analytics Engineer",
        case_type="analysis",
        tools=["Python", "SQL", "Grafana"],
        deadline_hours=60,
        urgency="urgent",
        deliverables=[
            DeliverableSpec(
                name="Performance Analysis Report",
                description="Trend analysis and anomaly detection results",
                file_types=[".pdf", ".xlsx"],
                naming_rule="performance_analysis_<yyyymmdd>.pdf",
                sheets=[],
                calc_rules=[],
            ),
            DeliverableSpec(
                name="Root Cause Findings",
                description="Detailed findings and recommendations",
                file_types=[".docx", ".pdf"],
                naming_rule="root_cause_<yyyymmdd>.pdf",
                sheets=[],
                calc_rules=[],
            ),
        ],
        rubric={
            "completeness": 25,
            "analytical_rigor": 35,
            "insight_quality": 25,
            "communication": 15,
        },
    ),
    Case(
        id="case-marketing-funnel",
        version="v1",
        title="Marketing Funnel Attribution and Cohort Performance",
        context=(
            "Direct-to-consumer brand wants clear attribution across paid, organic, and referral, plus cohort retention and CAC/LTV by channel."
        ),
        role="Marketing Data Analyst",
        case_type="analysis",
        tools=["SQL", "Python", "Looker"],
        deadline_hours=72,
        urgency="normal",
        deliverables=[
            DeliverableSpec(
                name="Attribution and Cohort Report",
                description="Channel attribution, CAC/LTV, and cohort retention by channel",
                file_types=[".xlsx", ".pdf"],
                naming_rule="funnel_attribution_<yyyymmdd>.xlsx",
                sheets=[],
                calc_rules=[],
            ),
            DeliverableSpec(
                name="Experiment Readout",
                description="A/B test results with lift, confidence, and next steps",
                file_types=[".pdf", ".docx"],
                naming_rule="experiment_readout_<yyyymmdd>.pdf",
                sheets=[],
                calc_rules=[],
            ),
        ],
        rubric={
            "completeness": 25,
            "methodology": 30,
            "insight_quality": 30,
            "communication": 15,
        },
    ),
    Case(
        id="case-ops-sla-quality",
        version="v1",
        title="Operations SLA, Quality, and Cycle Time Analysis",
        context=(
            "Customer support org needs SLA compliance, backlog aging, and quality metrics with root-cause breakdown by queue and region."
        ),
        role="Operations Data Analyst",
        case_type="analysis",
        tools=["SQL", "Python", "Tableau"],
        deadline_hours=72,
        urgency="high",
        deliverables=[
            DeliverableSpec(
                name="SLA and Backlog Dashboard",
                description="SLA attainment, backlog aging, and cycle time by queue/region",
                file_types=[".xlsx", ".pdf"],
                naming_rule="sla_backlog_<yyyymmdd>.xlsx",
                sheets=[],
                calc_rules=[],
            ),
            DeliverableSpec(
                name="Quality and Root Cause Report",
                description="QA scores, re-open rates, and top drivers of misses",
                file_types=[".docx", ".pdf"],
                naming_rule="quality_rootcause_<yyyymmdd>.pdf",
                sheets=[],
                calc_rules=[],
            ),
        ],
        rubric={
            "completeness": 25,
            "analytical_rigor": 30,
            "insight_quality": 30,
            "communication": 15,
        },
    ),
    Case(
        id="case-api-performance-nonprofit",
        version="v1",
        title="API Performance Investigation and Request/Response Time Analysis",
        context=(
            "Nonprofit organization providing digital services is experiencing API performance degradation impacting user experience and mission-critical workflows. Investigate API response times, request throughput, error rates, and identify root causes affecting different service endpoints. Provide recommendations to optimize performance and ensure reliability."
        ),
        role="Backend Performance Engineer",
        case_type="analysis",
        tools=["Python", "SQL", "Datadog", "Grafana"],
        deadline_hours=60,
        urgency="urgent",
        deliverables=[
            DeliverableSpec(
                name="API Performance Analysis Report",
                description="Comprehensive request/response time analysis by endpoint, latency distribution, and performance trends",
                file_types=[".pdf", ".xlsx"],
                naming_rule="api_performance_analysis_<yyyymmdd>.pdf",
                sheets=[
                    SheetRule(
                        name="Endpoint Metrics",
                        required_columns=["Endpoint", "Avg Response Time (ms)", "P95 Latency", "P99 Latency", "Error Rate %", "Throughput (req/s)"]
                    ),
                    SheetRule(
                        name="Time Series",
                        required_columns=["Timestamp", "Response Time", "Request Count", "Error Count", "Database Query Time"]
                    ),
                ],
                calc_rules=["Response time percentiles calculated from request logs", "Error rate = total errors / total requests"]
            ),
            DeliverableSpec(
                name="Root Cause Analysis",
                description="Identified bottlenecks, affected endpoints, and service dependencies",
                file_types=[".docx", ".pdf"],
                naming_rule="api_rootcause_<yyyymmdd>.pdf",
                sheets=[],
                calc_rules=[],
            ),
            DeliverableSpec(
                name="Performance Optimization Roadmap",
                description="Prioritized recommendations with implementation effort and expected impact",
                file_types=[".docx", ".xlsx"],
                naming_rule="optimization_roadmap_<yyyymmdd>.docx",
                sheets=[],
                calc_rules=[],
            ),
        ],
        rubric={
            "completeness": 25,
            "analytical_rigor": 35,
            "root_cause_identification": 25,
            "communication": 15,
        },
    ),
]


def get_case_by_id(case_id: str) -> Optional[Case]:
    for case in SAMPLE_CASES:
        if case.id == case_id:
            return case
    return None
