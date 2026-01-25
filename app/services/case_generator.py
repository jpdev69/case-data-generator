import random
from datetime import datetime
from typing import List

from app.schemas.cases import Case, DeliverableSpec, ObjectiveSpec, SheetRule


# Case templates with placeholders for randomization
CASE_TEMPLATES = [
    {
        "title_template": "Monthly {metric} Analysis for {company_type}",
        "context_template": "{company_type} needs {need}. Create a {metric} report with detailed breakdown.",
        "role_options": ["Financial Support VA", "Finance Operations Analyst", "Revenue Analyst VA"],
        "tools_pool": ["Excel", "Google Sheets", "HubSpot", "QuickBooks", "Notion", "Airtable"],
        "deliverable_count": (3, 5),
        "metric": ["Cash Flow", "Budget Variance", "Revenue Forecast", "Expense Analysis"],
    }
]

COMPANY_TYPES = [
    "SaaS startup",
    "E-commerce business",
    "Digital agency",
    "Consulting firm",
    "Marketplace platform",
    "B2B service provider",
    "Fintech company",
    "Logistics startup",
    "Healthcare provider",
    "Real estate firm",
    "Manufacturing company",
    "Subscription box service",
    "Staffing agency",
    "Software development shop",
    "Mobile app studio",
    "Nonprofit organization",
    "Recruitment firm",
    "Marketing agency",
    "Accounting practice",
    "Insurance brokerage",
    "EdTech platform",
    "Travel & hospitality",
    "Cybersecurity firm",
    "AI/ML startup",
    "Biotech company",
    "Sustainability company",
    "Fashion & retail",
    "Food & beverage",
    "Automotive supplier",
    "Construction firm",
]

FINANCIAL_NEEDS = [
    "runway clarity and AR hygiene",
    "budget reconciliation for investor due diligence",
    "quarterly financial health snapshot",
    "expense categorization and cost analysis",
    "customer profitability analysis",
    "cash flow forecasting for the next quarter",
    "payroll reconciliation and tax compliance check",
    "subscription revenue tracking and churn analysis",
    "invoice aging and collection improvement",
    "cost allocation across departments",
    "variance analysis against budget",
    "customer acquisition cost (CAC) analysis",
    "monthly recurring revenue (MRR) tracking",
    "accounts payable optimization",
    "working capital improvement plan",
    "sales pipeline revenue projection",
    "contract profitability assessment",
    "unit economics deep dive",
    "burn rate analysis and runway calculation",
    "pricing strategy validation through margin analysis",
    "sales commission reconciliation and audit",
    "tax position analysis and planning",
    "debt covenant compliance verification",
    "intercompany transaction elimination",
    "asset impairment assessment",
    "foreign exchange exposure analysis",
    "balance sheet health evaluation",
    "profitability by product line",
    "customer lifetime value (LTV) calculation",
    "gross margin trend analysis",
]

DATA_ANALYSIS_PROBLEMS = [
    "identify bottlenecks in customer onboarding process causing 35% drop-off rate",
    "analyze sales pipeline data to find why deals are stalling at proposal stage",
    "investigate operational inefficiencies causing 40% increase in support ticket resolution time",
    "detect data quality issues impacting marketing attribution accuracy",
    "identify patterns in product usage that reveal feature adoption gaps",
    "analyze customer churn patterns to identify at-risk segments",
    "find root causes of declining user engagement across product features",
    "investigate inconsistencies in reported metrics across different departments",
    "analyze hiring data to identify bottlenecks in recruitment process",
    "identify performance bottlenecks in application by analyzing system logs",
    "analyze website traffic to discover why conversion rate is declining",
    "investigate inventory management issues causing overstocking and stockouts",
    "identify behavioral patterns in customer complaints to address systemic issues",
    "analyze employee productivity data to find efficiency gaps by team",
    "investigate data inconsistencies between CRM and accounting systems",
    "identify seasonal patterns affecting demand forecasting accuracy",
    "analyze customer segmentation to optimize marketing spend allocation",
    "investigate API performance issues through request/response time analysis",
    "identify gaps in data collection impacting business intelligence reporting",
    "analyze delivery logistics data to find route optimization opportunities",
    "detect fraud patterns in transaction data across multiple channels",
    "analyze customer retention metrics to identify at-risk cohorts",
    "investigate supplier performance issues affecting delivery times",
    "identify marketing campaign underperformance through attribution analysis",
    "analyze mobile app user behavior to improve feature discoverability",
    "detect anomalies in financial transactions indicating control weaknesses",
    "analyze employee turnover data to identify retention risks",
    "investigate quality control failures in manufacturing process",
    "identify cross-sell opportunities through customer purchase pattern analysis",
    "analyze social media sentiment to track brand health trends",
]

DELIVERABLE_TEMPLATES = [
    {
        "name": "Summary Report",
        "description": "High-level overview with key metrics and trends",
        "file_types": [".xlsx", ".pdf"],
    },
    {
        "name": "Detailed Analysis Workbook",
        "description": "Multi-sheet workbook with calculations and breakdowns",
        "file_types": [".xlsx"],
    },
    {
        "name": "Variance/Reconciliation Report",
        "description": "Comparison against benchmarks or prior periods",
        "file_types": [".xlsx", ".csv"],
    },
    {
        "name": "Executive Brief",
        "description": "One-page summary with key insights and recommendations",
        "file_types": [".pdf", ".docx"],
    },
    {
        "name": "Data Export",
        "description": "Clean, formatted data for further analysis or integration",
        "file_types": [".csv", ".xlsx"],
    },
    {
        "name": "Issues and Risks Log",
        "description": "Documented anomalies, compliance items, and action items",
        "file_types": [".pdf", ".docx"],
    },
    {
        "name": "Trend Analysis Chart",
        "description": "Visual representation of key metrics over time",
        "file_types": [".xlsx", ".pdf"],
    },
    {
        "name": "Customer Segment Report",
        "description": "Breakdown of metrics by customer tier or segment",
        "file_types": [".xlsx"],
    },
    {
        "name": "Forecast Model",
        "description": "Projections for upcoming months or quarters",
        "file_types": [".xlsx"],
    },
    {
        "name": "Reconciliation Schedule",
        "description": "Detailed line-by-line reconciliation",
        "file_types": [".xlsx"],
    },
    {
        "name": "Compliance Checklist",
        "description": "Verification of regulatory and internal policy adherence",
        "file_types": [".pdf", ".xlsx"],
    },
    {
        "name": "Action Items Register",
        "description": "Prioritized list of follow-ups and next steps",
        "file_types": [".xlsx", ".docx"],
    },
]

DATA_ANALYSIS_DELIVERABLES = [
    {
        "name": "Root Cause Analysis Report",
        "description": "Identify underlying causes of identified bottlenecks and problems",
        "file_types": [".pdf", ".docx"],
    },
    {
        "name": "Problem Diagnosis Dashboard",
        "description": "Interactive dashboard showing key metrics and problem areas",
        "file_types": [".xlsx", ".pdf"],
    },
    {
        "name": "Data Quality Assessment",
        "description": "Analysis of data completeness, accuracy, and consistency issues",
        "file_types": [".xlsx", ".pdf"],
    },
    {
        "name": "Anomaly Detection Report",
        "description": "Identified outliers and unusual patterns in the data",
        "file_types": [".xlsx", ".pdf"],
    },
    {
        "name": "Process Bottleneck Analysis",
        "description": "Detailed breakdown of where processes are failing or slowing",
        "file_types": [".pdf", ".docx"],
    },
    {
        "name": "Recommendations & Action Plan",
        "description": "Specific, prioritized recommendations to address identified issues",
        "file_types": [".pdf", ".docx"],
    },
    {
        "name": "Comparative Analysis",
        "description": "Benchmarking against industry standards or historical performance",
        "file_types": [".xlsx", ".pdf"],
    },
    {
        "name": "Data Correlation Study",
        "description": "Analysis of relationships between variables contributing to problems",
        "file_types": [".xlsx"],
    },
    {
        "name": "Performance Bottleneck Visualization",
        "description": "Visual charts highlighting where systems are underperforming",
        "file_types": [".pdf", ".xlsx"],
    },
    {
        "name": "Segmentation & Clustering Analysis",
        "description": "Group data by characteristics to identify problem segments",
        "file_types": [".xlsx", ".pdf"],
    },
]

URGENCY_OPTIONS = ["normal", "high", "urgent"]
DEADLINE_HOURS = [48, 60, 72, 96]

RUBRIC_TEMPLATES = [
    {"completeness": 25, "structure": 25, "financial_logic": 30, "communication": 20},
    {"completeness": 30, "structure": 20, "financial_logic": 30, "communication": 20},
    {"completeness": 25, "structure": 20, "financial_logic": 35, "communication": 20},
]

DATA_ANALYSIS_RUBRIC_TEMPLATES = [
    {"problem_identification": 30, "root_cause_analysis": 25, "data_quality": 20, "recommendations": 25},
    {"problem_identification": 25, "root_cause_analysis": 30, "data_quality": 20, "recommendations": 25},
    {"problem_identification": 30, "root_cause_analysis": 20, "data_quality": 25, "recommendations": 25},
]

# Objective templates for financial VA cases
FINANCIAL_OBJECTIVES_TEMPLATES = [
    {
        "title": "Data Validation & Reconciliation",
        "description": "Ensure all source data is complete, accurate, and reconciles to control totals",
        "success_criteria": [
            "All transactions reconcile to source systems",
            "No missing or duplicate records",
            "All discrepancies documented and explained",
        ]
    },
    {
        "title": "Analysis & Insight Generation",
        "description": "Perform detailed analysis to uncover key trends, outliers, and business insights",
        "success_criteria": [
            "Identified top 5 drivers of variance or change",
            "Month-over-month and year-over-year trends analyzed",
            "Outliers and anomalies documented with explanations",
        ]
    },
    {
        "title": "Executive Summary Creation",
        "description": "Develop clear, concise summary communicating key findings to stakeholders",
        "success_criteria": [
            "1-page executive summary with key metrics highlighted",
            "Top 3 recommendations provided",
            "Impact quantified in business terms",
        ]
    },
    {
        "title": "Documentation & Support",
        "description": "Prepare comprehensive documentation explaining methodology and calculations",
        "success_criteria": [
            "Calculation logic clearly documented",
            "Data dictionary provided for all metrics",
            "Assumptions and limitations outlined",
        ]
    },
    {
        "title": "Stakeholder Communication",
        "description": "Present findings and recommendations in a clear, actionable manner",
        "success_criteria": [
            "Key findings explained in business context",
            "Recommended actions with expected outcomes",
            "Timeline for implementation provided",
        ]
    },
]

# Objective templates for data analysis cases
DATA_ANALYSIS_OBJECTIVES_TEMPLATES = [
    {
        "title": "Problem Diagnosis",
        "description": "Clearly identify and document the specific problem, its scope, and impact",
        "success_criteria": [
            "Problem statement is measurable and specific",
            "Affected customer/user segments identified",
            "Business impact quantified with current metrics",
        ]
    },
    {
        "title": "Root Cause Analysis",
        "description": "Investigate underlying causes using data-driven evidence",
        "success_criteria": [
            "Multiple hypotheses tested with data",
            "Root causes prioritized by impact",
            "Correlation vs causation clearly distinguished",
        ]
    },
    {
        "title": "Data Quality Assessment",
        "description": "Evaluate data completeness, accuracy, and consistency issues",
        "success_criteria": [
            "Data quality issues identified and quantified",
            "Impact on analysis documented",
            "Data limitations acknowledged",
        ]
    },
    {
        "title": "Recommendations Development",
        "description": "Create specific, actionable recommendations to address identified issues",
        "success_criteria": [
            "3-5 prioritized recommendations with business case",
            "Expected impact quantified for each recommendation",
            "Implementation considerations outlined",
        ]
    },
    {
        "title": "Results Presentation",
        "description": "Present analysis in clear, visual format for stakeholder consumption",
        "success_criteria": [
            "Key findings presented visually with charts/dashboards",
            "Executive summary with key metrics highlighted",
            "Recommendations ranked by effort vs impact",
        ]
    },
]


def _generate_financial_objectives() -> List[ObjectiveSpec]:
    """Generate 3-4 generic objectives for a financial VA case."""
    num_objectives = random.randint(3, 4)
    selected_templates = random.sample(FINANCIAL_OBJECTIVES_TEMPLATES, min(num_objectives, len(FINANCIAL_OBJECTIVES_TEMPLATES)))
    
    return [
        ObjectiveSpec(
            title=template["title"],
            description=template["description"],
            success_criteria=template["success_criteria"]
        )
        for template in selected_templates
    ]


def _generate_data_analysis_objectives() -> List[ObjectiveSpec]:
    """Generate 3-4 generic objectives for a data analysis case."""
    num_objectives = random.randint(3, 4)
    selected_templates = random.sample(DATA_ANALYSIS_OBJECTIVES_TEMPLATES, min(num_objectives, len(DATA_ANALYSIS_OBJECTIVES_TEMPLATES)))
    
    return [
        ObjectiveSpec(
            title=template["title"],
            description=template["description"],
            success_criteria=template["success_criteria"]
        )
        for template in selected_templates
    ]


def _generate_financial_objectives_contextual(case: Case) -> List[ObjectiveSpec]:
    """Generate context-aware objectives for a financial VA case based on deliverables and case details."""
    objectives = []
    
    # Extract case-specific information
    company_type = case.title.split(" for ")[-1] if " for " in case.title else "your company"
    metric = case.title.split(" ")[0] if " " in case.title else "financial data"
    deliverable_names = [d.name for d in case.deliverables]
    tools_str = ", ".join(case.tools) if case.tools else "available tools"
    
    # Objective 1: Data validation specific to case
    objectives.append(ObjectiveSpec(
        title="Data Collection & Validation",
        description=f"Gather and validate {metric.lower()} data for {company_type} from relevant source systems. Ensure all transactions, balances, and supporting documentation are complete and accurate.",
        success_criteria=[
            f"All {metric.lower()} data extracted from source systems and reconciled to control totals",
            "Missing or incomplete records identified and documented",
            "Data quality issues logged with root cause analysis",
            "Variance explanations documented for any discrepancies found"
        ]
    ))
    
    # Objective 2: Analysis focused on deliverables
    if any("Report" in d or "Analysis" in d for d in deliverable_names):
        analysis_deliverables = [d for d in deliverable_names if "Analysis" in d or "Report" in d]
        objectives.append(ObjectiveSpec(
            title="Comprehensive Analysis & Breakdown",
            description=f"Perform detailed {metric.lower()} analysis for {company_type} using {tools_str}. Create the following deliverables: {', '.join(analysis_deliverables[:2])}. Identify key drivers, trends, and anomalies.",
            success_criteria=[
                f"Month-over-month and year-over-year {metric.lower()} trends analyzed and visualized",
                "Top 5 drivers of variance identified with quantified impact",
                "Seasonal patterns, outliers, and anomalies documented with explanations",
                "Analysis methodology clearly documented with assumptions stated"
            ]
        ))
    
    # Objective 3: Reconciliation and validation
    if any("Reconciliation" in d or "Variance" in d for d in deliverable_names):
        objectives.append(ObjectiveSpec(
            title="Reconciliation & Variance Analysis",
            description=f"Reconcile {metric.lower()} figures across all source systems and prepare detailed reconciliation schedule. Explain all variances from budget, prior period, or benchmarks.",
            success_criteria=[
                "Line-by-line reconciliation completed with 100% balance achieved",
                "All variance explanations supported by documentation",
                f"Variance analysis shows impact on {company_type} financial position",
                "Reconciliation schedule updated for stakeholder review"
            ]
        ))
    
    # Objective 4: Executive summary and recommendations
    if any("Brief" in d or "Summary" in d for d in deliverable_names):
        objectives.append(ObjectiveSpec(
            title="Executive Summary & Recommendations",
            description=f"Develop clear, concise executive summary communicating {metric.lower()} analysis findings to stakeholders of {company_type}. Provide 3-5 actionable recommendations.",
            success_criteria=[
                "1-page executive summary with key metrics and findings highlighted",
                "Top 3 recommendations with business case and expected impact quantified",
                "Recommended actions prioritized by effort vs. impact",
                "Implementation timeline and resource requirements outlined"
            ]
        ))
    
    return objectives[:4]  # Return max 4 objectives


def _generate_data_analysis_objectives_contextual(case: Case) -> List[ObjectiveSpec]:
    """Generate context-aware objectives for a data analysis case based on the problem and deliverables."""
    objectives = []
    
    # Extract case-specific information
    context_words = case.context.split()
    company_type = case.title.split(" for ")[-1] if " for " in case.title else "the organization"
    problem_phrase = case.context.split("needs you to ")[-1].split(".")[0] if "needs you to" in case.context else "address the identified issues"
    deliverable_names = [d.name for d in case.deliverables]
    tools_str = ", ".join(case.tools) if case.tools else "analytical tools"
    
    # Objective 1: Problem diagnosis
    objectives.append(ObjectiveSpec(
        title="Problem Identification & Scoping",
        description=f"Clearly define the business problem for {company_type}: {problem_phrase}. Quantify the impact and identify all affected customer segments or business areas.",
        success_criteria=[
            f"Problem statement for {company_type} is specific and measurable with clear metrics",
            "Affected customer segments or business areas quantified with current performance metrics",
            "Business impact in terms of revenue, cost, or efficiency losses calculated",
            "Scope boundaries clearly defined (time period, data range, affected systems)"
        ]
    ))
    
    # Objective 2: Root cause analysis
    if any("Root Cause" in d or "Diagnosis" in d for d in deliverable_names):
        objectives.append(ObjectiveSpec(
            title="Root Cause Analysis",
            description=f"Investigate and document the underlying causes of the {problem_phrase} at {company_type}. Test multiple hypotheses using {tools_str} and prioritize root causes by impact.",
            success_criteria=[
                f"3-5 root causes identified for {problem_phrase} with supporting data evidence",
                "Each root cause validated with at least 2 independent data sources",
                "Root causes ranked by business impact (revenue, cost, customer satisfaction)",
                "Correlation vs. causation clearly distinguished with methodology explained"
            ]
        ))
    
    # Objective 3: Data quality and anomaly detection
    if any("Quality" in d or "Anomaly" in d for d in deliverable_names):
        objectives.append(ObjectiveSpec(
            title="Data Quality Assessment & Anomaly Detection",
            description=f"Evaluate data completeness, accuracy, and consistency for {company_type}. Identify data quality issues that may have contributed to {problem_phrase}.",
            success_criteria=[
                "Data quality issues (null values, duplicates, inconsistencies) quantified by severity",
                "Impact of each data quality issue on analysis and business decisions documented",
                "Anomalies and outliers in the dataset identified with explanations",
                "Data limitations acknowledged and their impact on conclusions stated"
            ]
        ))
    
    # Objective 4: Actionable recommendations
    if any("Recommendation" in d or "Action" in d for d in deliverable_names):
        objectives.append(ObjectiveSpec(
            title="Recommendations & Action Plan",
            description=f"Develop 3-5 specific, prioritized recommendations to address the identified issues at {company_type}. Quantify expected business impact for each recommendation.",
            success_criteria=[
                f"3-5 recommendations to resolve {problem_phrase} with clear business cases",
                "Expected impact for each recommendation quantified (revenue, cost savings, efficiency gains)",
                "Implementation effort and resource requirements estimated (effort/time/cost)",
                "Quick wins identified and ranked by effort vs. impact"
            ]
        ))
    
    return objectives[:4]  # Return max 4 objectives



def generate_random_case() -> Case:
    """Generate a random practice case - either financial VA or data analysis."""
    # Randomly choose between financial and data analysis cases (50/50)
    if random.choice([True, False]):
        return _generate_financial_case()
    else:
        return generate_data_analysis_case()


def _generate_financial_case() -> Case:
    """Generate a unique, realistic financial VA practice case."""

    case_id = f"case-{datetime.now().strftime('%Y%m%d%H%M%S')}-{random.randint(1000, 9999)}"
    company_type = random.choice(COMPANY_TYPES)
    financial_need = random.choice(FINANCIAL_NEEDS)
    metric = random.choice(["Cash Flow", "Budget", "Revenue", "Expense", "Payroll", "Profitability", "Forecast", "Reconciliation"])
    role = random.choice(["Financial Support VA", "Finance Operations Analyst", "Revenue Analyst VA", "Payroll Analyst", "FP&A Associate"])

    if metric == "Profitability":
        title = f"Profitability Analysis for {company_type}"
        context = f"{company_type.capitalize()} needs {financial_need}. Assess unit economics and margin performance by product and segment with clear allocation methodology."
    elif metric == "Reconciliation":
        title = f"Financial Reconciliation for {company_type}"
        context = f"{company_type.capitalize()} needs {financial_need}. Reconcile source transactions to ledger control totals, document variances and unmatched items, and provide resolution steps."
    else:
        title = f"{metric} Analysis & Reconciliation for {company_type}"
        context = f"{company_type.capitalize()} needs {financial_need}. Prepare detailed {metric.lower()} analysis with actionable recommendations."

    # Select 3-5 random deliverables
    num_deliverables = random.randint(3, 5)
    selected_deliverables = random.sample(DELIVERABLE_TEMPLATES, min(num_deliverables, len(DELIVERABLE_TEMPLATES)))

    deliverables = []
    for deliv in selected_deliverables:
        spec = DeliverableSpec(
            name=deliv["name"],
            description=deliv["description"],
            file_types=deliv["file_types"],
            required_count=1,
            sheets=[
                SheetRule(name="Data", required_columns=["Date", "Amount", "Category", "Status"]),
            ] if ".xlsx" in deliv["file_types"] else [],
            calc_rules=["Totals must reconcile"] if ".xlsx" in deliv["file_types"] else [],
        )
        deliverables.append(spec)

    # Select 2-4 random tools
    num_tools = random.randint(2, 4)
    tools = random.sample(["Excel", "Google Sheets", "QuickBooks", "HubSpot", "Notion", "Airtable", "Python", "Tableau", "Power BI", "Stripe", "Salesforce"], num_tools)

    urgency = random.choice(URGENCY_OPTIONS)
    deadline_hours = random.choice(DEADLINE_HOURS)

    rubric = random.choice(RUBRIC_TEMPLATES)

    return Case(
        id=case_id,
        version="v1",
        title=title,
        context=context,
        role=role,
        case_type="financial",
        tools=tools,
        deadline_hours=deadline_hours,
        urgency=urgency,
        deliverables=deliverables,
        objectives=_generate_financial_objectives(),
        rubric=rubric,
    )


def generate_data_analysis_case() -> Case:
    """Generate a unique, realistic data analysis case focused on identifying business problems and bottlenecks."""

    case_id = f"case-{datetime.now().strftime('%Y%m%d%H%M%S')}-{random.randint(1000, 9999)}"
    company_type = random.choice(COMPANY_TYPES)
    problem = random.choice(DATA_ANALYSIS_PROBLEMS)
    role = random.choice(["Data Analyst", "Business Analyst", "Operations Analyst", "Product Analytics", "Data Scientist", "Analytics Engineer"])

    title = f"Problem Identification & Analysis for {company_type}"
    context = f"{company_type.capitalize()} is experiencing issues and needs you to {problem}. Provide comprehensive analysis identifying root causes, affected business areas, and recommend solutions."

    # Select 3-5 random data analysis deliverables
    num_deliverables = random.randint(3, 5)
    selected_deliverables = random.sample(DATA_ANALYSIS_DELIVERABLES, min(num_deliverables, len(DATA_ANALYSIS_DELIVERABLES)))

    deliverables = []
    for deliv in selected_deliverables:
        spec = DeliverableSpec(
            name=deliv["name"],
            description=deliv["description"],
            file_types=deliv["file_types"],
            required_count=1,
            sheets=[
                SheetRule(name="Analysis", required_columns=["Metric", "Current_Value", "Benchmark", "Variance", "Root_Cause"]),
                SheetRule(name="Recommendations", required_columns=["Issue", "Priority", "Recommendation", "Expected_Impact", "Timeline"]),
            ] if ".xlsx" in deliv["file_types"] else [],
            calc_rules=["Impact calculations must be accurate", "Variance calculations must show trend direction"] if ".xlsx" in deliv["file_types"] else [],
        )
        deliverables.append(spec)

    # Select 2-4 random analysis tools
    num_tools = random.randint(2, 4)
    tools = random.sample(["Python", "SQL", "Excel", "Google Sheets", "Tableau", "Power BI", "R", "Looker", "Google Analytics", "Mixpanel", "Amplitude"], num_tools)

    urgency = random.choice(URGENCY_OPTIONS)
    deadline_hours = random.choice(DEADLINE_HOURS)

    rubric = random.choice(DATA_ANALYSIS_RUBRIC_TEMPLATES)

    return Case(
        id=case_id,
        version="v1",
        title=title,
        context=context,
        role=role,
        case_type="analysis",
        tools=tools,
        deadline_hours=deadline_hours,
        urgency=urgency,
        deliverables=deliverables,
        objectives=_generate_data_analysis_objectives(),
        rubric=rubric,
    )


def calculate_case_generation_capacity() -> dict:
    """
    Calculate theoretical maximum unique cases that can be generated.
    
    Returns:
        dict with breakdown of unique case combinations
    """
    from math import comb, factorial
    
    # Financial Case Parameters
    financial_company_types = len(COMPANY_TYPES)  # 30
    financial_needs = len(FINANCIAL_NEEDS)  # 30
    financial_metrics = 8
    financial_roles = 5
    financial_deadlines = len(DEADLINE_HOURS)  # 4
    financial_urgency = len(URGENCY_OPTIONS)  # 3
    financial_tools = 11
    financial_deliverables = 12
    financial_rubrics = len(RUBRIC_TEMPLATES)  # 3
    
    # Tool combinations (choosing 2-4 from 11)
    tool_combos = (
        comb(financial_tools, 2) + comb(financial_tools, 3) + comb(financial_tools, 4)
    )
    
    # Deliverable combinations (choosing 3-5 from 12)
    deliverable_combos = (
        comb(financial_deliverables, 3) + comb(financial_deliverables, 4) + comb(financial_deliverables, 5)
    )
    
    financial_base = (
        financial_company_types * 
        financial_needs * 
        financial_metrics * 
        financial_roles * 
        financial_deadlines * 
        financial_urgency * 
        financial_rubrics
    )
    
    financial_with_combos = financial_base * tool_combos * deliverable_combos
    
    # Data Analysis Case Parameters
    data_company_types = len(COMPANY_TYPES)  # 30
    data_problems = len(DATA_ANALYSIS_PROBLEMS)  # 30
    data_roles = 6
    data_deadlines = len(DEADLINE_HOURS)  # 4
    data_urgency = len(URGENCY_OPTIONS)  # 3
    data_tools = 11
    data_deliverables = 10
    data_rubrics = len(DATA_ANALYSIS_RUBRIC_TEMPLATES)  # 3
    
    # Tool combinations (choosing 2-4 from 11)
    data_tool_combos = tool_combos
    
    # Deliverable combinations (choosing 3-5 from 10)
    data_deliverable_combos = (
        comb(data_deliverables, 3) + comb(data_deliverables, 4) + comb(data_deliverables, 5)
    )
    
    data_base = (
        data_company_types * 
        data_problems * 
        data_roles * 
        data_deadlines * 
        data_urgency * 
        data_rubrics
    )
    
    data_with_combos = data_base * data_tool_combos * data_deliverable_combos
    
    total = financial_with_combos + data_with_combos
    
    return {
        "financial_cases": {
            "base_combinations": financial_base,
            "with_tool_deliverable_combos": int(financial_with_combos),
            "company_types": financial_company_types,
            "financial_needs": financial_needs,
            "metrics": financial_metrics,
            "roles": financial_roles,
            "deadline_options": financial_deadlines,
            "urgency_levels": financial_urgency,
            "tool_combinations": int(tool_combos),
            "deliverable_combinations": int(deliverable_combos),
            "rubric_templates": financial_rubrics,
        },
        "data_analysis_cases": {
            "base_combinations": data_base,
            "with_tool_deliverable_combos": int(data_with_combos),
            "company_types": data_company_types,
            "problem_scenarios": data_problems,
            "roles": data_roles,
            "deadline_options": data_deadlines,
            "urgency_levels": data_urgency,
            "tool_combinations": int(data_tool_combos),
            "deliverable_combinations": int(data_deliverable_combos),
            "rubric_templates": data_rubrics,
        },
        "total_unique_cases": int(total),
        "timestamp_variation": "Additional uniqueness from millisecond-precision timestamps"
    }
