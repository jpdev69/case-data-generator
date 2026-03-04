import random
from datetime import datetime
from typing import List

from app.schemas.cases import Case, DeliverableSpec, ObjectiveSpec, SheetRule


# ---------------------------------------------------------------------------
# DATA PROFILES – each profile bundles a coherent set of:
#   title templates, context needs, deliverables (with correct sheet defs),
#   role options, tool pools, and rubric weights.
# The mock-data generator dispatches on the profile key so the dataset
# always matches the case scenario.
# ---------------------------------------------------------------------------

FINANCIAL_PROFILES = {
    # ---- Cash Flow / Runway / AR ------------------------------------------
    "cashflow": {
        "title_templates": [
            "Monthly Cash Flow and Receivables Hygiene for {company}",
            "Cash Flow Forecasting and AR Analysis for {company}",
            "Working Capital and Cash Position Review for {company}",
        ],
        "needs": [
            "runway clarity and AR hygiene",
            "cash flow forecasting for the next quarter",
            "invoice aging and collection improvement",
            "working capital improvement plan",
            "burn rate analysis and runway calculation",
            "balance sheet health evaluation",
        ],
        "context_template": "{company} needs {need}. Build a rolling cash-flow tracker, reconcile receivables, and flag runway risks.",
        "roles": ["Financial Support VA", "Finance Operations Analyst", "FP&A Associate"],
        "tools_pool": ["Excel", "Google Sheets", "QuickBooks", "HubSpot", "Stripe"],
        "deliverables": [
            DeliverableSpec(
                name="Monthly Cash Flow Tracker",
                description="12-week rolling cash flow with receipts vs disbursements",
                file_types=[".xlsx"],
                sheets=[
                    SheetRule(name="Summary", required_columns=["Week", "Inflows", "Outflows", "Net", "Balance"]),
                    SheetRule(name="Receipts", required_columns=["Date", "Customer", "Amount", "Category", "Status"]),
                ],
                calc_rules=["Balance rolls forward from prior week", "Net = Inflows - Outflows"],
            ),
            DeliverableSpec(
                name="Invoice and AR Detail",
                description="AR aging with invoice-level detail",
                file_types=[".xlsx"],
                sheets=[
                    SheetRule(name="Aging", required_columns=["Customer", "Invoice", "Issued", "Due", "Amount", "Bucket"]),
                ],
                calc_rules=["Aging bucket derived from due date"],
            ),
            DeliverableSpec(
                name="Disbursements Log",
                description="Detailed outgoing payments by vendor, category, and status",
                file_types=[".xlsx", ".csv"],
                sheets=[
                    SheetRule(name="Disbursements", required_columns=["Date", "Vendor", "Category", "Amount", "Status"]),
                ],
                calc_rules=[],
            ),
            DeliverableSpec(
                name="Executive Summary",
                description="Narrative summary of cash position risks and recommendations",
                file_types=[".pdf", ".docx"],
                sheets=[],
                calc_rules=[],
            ),
        ],
        "rubric": {"completeness": 25, "structure": 25, "financial_logic": 30, "communication": 20},
    },

    # ---- Expense Audit / Budget Variance ----------------------------------
    "expense_audit": {
        "title_templates": [
            "Quarterly Expense Audit and Budget Reconciliation for {company}",
            "Budget Variance Analysis and Cost Optimization for {company}",
            "Expense Categorization and Departmental Spend Review for {company}",
        ],
        "needs": [
            "budget reconciliation for investor due diligence",
            "expense categorization and cost analysis",
            "cost allocation across departments",
            "variance analysis against budget",
            "accounts payable optimization",
        ],
        "context_template": "{company} needs {need}. Categorise expenses by department, calculate budget variance, and flag anomalies.",
        "roles": ["Finance Operations Analyst", "FP&A Associate", "Financial Support VA"],
        "tools_pool": ["Excel", "QuickBooks", "Google Sheets", "Notion", "Airtable"],
        "deliverables": [
            DeliverableSpec(
                name="Expense Report by Category",
                description="Quarterly expenses broken down by department and category",
                file_types=[".xlsx"],
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
                sheets=[
                    SheetRule(name="Dashboard", required_columns=["Department", "Budget", "Actual", "Variance", "Variance %"]),
                ],
                calc_rules=[],
            ),
            DeliverableSpec(
                name="Findings Report",
                description="Written summary of anomalies and recommendations",
                file_types=[".pdf"],
                sheets=[],
                calc_rules=[],
            ),
        ],
        "rubric": {"completeness": 30, "structure": 20, "financial_logic": 30, "communication": 20},
    },

    # ---- Revenue Forecast / MRR ------------------------------------------
    "revenue_forecast": {
        "title_templates": [
            "3-Month Revenue Forecast for {company}",
            "MRR Forecasting and Churn Analysis for {company}",
            "Revenue Projection and Scenario Modelling for {company}",
        ],
        "needs": [
            "quarterly financial health snapshot",
            "subscription revenue tracking and churn analysis",
            "monthly recurring revenue (MRR) tracking",
            "sales pipeline revenue projection",
            "pricing strategy validation through margin analysis",
            "customer lifetime value (LTV) calculation",
            "gross margin trend analysis",
        ],
        "context_template": "{company} needs {need}. Forecast MRR for the next 3 months factoring in churn, expansion, and new sign-ups.",
        "roles": ["Revenue Analyst VA", "FP&A Associate", "Finance Operations Analyst"],
        "tools_pool": ["Excel", "Google Sheets", "Stripe", "Salesforce", "HubSpot"],
        "deliverables": [
            DeliverableSpec(
                name="Revenue Forecast Model",
                description="Rolling 3-month forecast with MRR, churn, and expansion revenue",
                file_types=[".xlsx"],
                sheets=[
                    SheetRule(name="Assumptions", required_columns=["Metric", "Value", "Source"]),
                    SheetRule(name="Forecast", required_columns=["Month", "New MRR", "Churn MRR", "Expansion MRR", "Total MRR"]),
                ],
                calc_rules=["Total MRR = Previous MRR + New - Churn + Expansion"],
            ),
            DeliverableSpec(
                name="Scenario Analysis",
                description="Best / worst / likely case scenarios",
                file_types=[".xlsx"],
                sheets=[
                    SheetRule(name="Scenarios", required_columns=["Scenario", "Growth Rate", "Churn Change", "Projected MRR"]),
                ],
                calc_rules=[],
            ),
            DeliverableSpec(
                name="Executive Brief",
                description="One-page summary with key insights",
                file_types=[".pdf", ".docx"],
                sheets=[],
                calc_rules=[],
            ),
        ],
        "rubric": {"completeness": 25, "structure": 20, "financial_logic": 35, "communication": 20},
    },

    # ---- Payroll / Tax Compliance -----------------------------------------
    "payroll": {
        "title_templates": [
            "Monthly Payroll Reconciliation and Compliance Check for {company}",
            "Payroll Audit and Tax Withholding Verification for {company}",
            "Contractor and Staff Pay Reconciliation for {company}",
        ],
        "needs": [
            "payroll reconciliation and tax compliance check",
            "sales commission reconciliation and audit",
            "tax position analysis and planning",
        ],
        "context_template": "{company} needs {need}. Reconcile payroll runs to bank statements, verify tax withholdings, and flag discrepancies.",
        "roles": ["Payroll & Compliance VA", "Payroll Analyst", "Finance Operations Analyst"],
        "tools_pool": ["Excel", "ADP", "Gusto", "QuickBooks"],
        "deliverables": [
            DeliverableSpec(
                name="Payroll Reconciliation Report",
                description="Month-end payroll totals reconciled against bank statements",
                file_types=[".xlsx"],
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
                sheets=[],
                calc_rules=[],
            ),
            DeliverableSpec(
                name="Issue Log",
                description="Document any discrepancies or compliance risks",
                file_types=[".pdf", ".docx"],
                sheets=[],
                calc_rules=[],
            ),
        ],
        "rubric": {"completeness": 30, "structure": 25, "financial_logic": 25, "communication": 20},
    },

    # ---- Profitability / Unit Economics -----------------------------------
    "profitability": {
        "title_templates": [
            "Profitability Analysis for {company}",
            "Unit Economics Deep Dive for {company}",
            "Product-Line Margin Analysis for {company}",
        ],
        "needs": [
            "customer profitability analysis",
            "contract profitability assessment",
            "unit economics deep dive",
            "profitability by product line",
            "customer acquisition cost (CAC) analysis",
        ],
        "context_template": "{company} needs {need}. Assess unit economics and margin performance by product and segment with clear allocation methodology.",
        "roles": ["FP&A Associate", "Revenue Analyst VA", "Finance Operations Analyst"],
        "tools_pool": ["Excel", "Google Sheets", "QuickBooks", "Stripe", "Salesforce"],
        "deliverables": [
            DeliverableSpec(
                name="Profitability Breakdown",
                description="Revenue, COGS, and margin by product / segment",
                file_types=[".xlsx"],
                sheets=[
                    SheetRule(name="Summary", required_columns=["Product/Segment", "Revenue", "COGS", "Gross Margin", "Margin %"]),
                    SheetRule(name="Details", required_columns=["Date", "Product", "Revenue", "Cost", "Contribution"]),
                ],
                calc_rules=["Gross Margin = Revenue - COGS", "Margin % = Gross Margin / Revenue"],
            ),
            DeliverableSpec(
                name="Unit Economics Model",
                description="CAC, LTV, and payback period calculations",
                file_types=[".xlsx"],
                sheets=[
                    SheetRule(name="Unit Economics", required_columns=["Metric", "Value", "Trend", "Benchmark"]),
                ],
                calc_rules=["LTV/CAC ratio computed"],
            ),
            DeliverableSpec(
                name="Executive Summary",
                description="Findings and margin-improvement recommendations",
                file_types=[".pdf", ".docx"],
                sheets=[],
                calc_rules=[],
            ),
        ],
        "rubric": {"completeness": 25, "structure": 25, "financial_logic": 30, "communication": 20},
    },

    # ---- Financial Reconciliation (general) --------------------------------
    "reconciliation": {
        "title_templates": [
            "Financial Reconciliation for {company}",
            "Multi-System Ledger Reconciliation for {company}",
            "Transaction Matching and Variance Resolution for {company}",
        ],
        "needs": [
            "debt covenant compliance verification",
            "intercompany transaction elimination",
            "asset impairment assessment",
            "foreign exchange exposure analysis",
        ],
        "context_template": "{company} needs {need}. Reconcile source transactions to ledger control totals, document variances and unmatched items, and provide resolution steps.",
        "roles": ["Financial Support VA", "Finance Operations Analyst", "FP&A Associate"],
        "tools_pool": ["Excel", "QuickBooks", "Google Sheets", "Airtable"],
        "deliverables": [
            DeliverableSpec(
                name="Reconciliation Schedule",
                description="Detailed line-by-line reconciliation",
                file_types=[".xlsx"],
                sheets=[
                    SheetRule(name="Reconciliation", required_columns=["Date", "Description", "Source Amount", "Ledger Amount", "Difference", "Status"]),
                ],
                calc_rules=["Difference = Source Amount - Ledger Amount", "All items must reconcile or be explained"],
            ),
            DeliverableSpec(
                name="Variance Summary",
                description="Grouped variance explanations by category",
                file_types=[".xlsx"],
                sheets=[
                    SheetRule(name="Variance", required_columns=["Category", "Total Variance", "Explained", "Unexplained"]),
                ],
                calc_rules=[],
            ),
            DeliverableSpec(
                name="Issues and Action Items",
                description="Documented anomalies, compliance items, and resolution steps",
                file_types=[".pdf", ".docx"],
                sheets=[],
                calc_rules=[],
            ),
        ],
        "rubric": {"completeness": 30, "structure": 25, "financial_logic": 25, "communication": 20},
    },
}


# ---------------------------------------------------------------------------
# DATA ANALYSIS PROFILES
# ---------------------------------------------------------------------------

DATA_ANALYSIS_PROFILES = {
    # ---- Customer Analytics / Segmentation --------------------------------
    "customer_analytics": {
        "title_templates": [
            "Customer Behavior Analytics and Segmentation for {company}",
            "Customer Churn and Retention Analysis for {company}",
            "Cohort-Based Customer Profitability Study for {company}",
        ],
        "problems": [
            "identify bottlenecks in customer onboarding process causing 35% drop-off rate",
            "analyze customer churn patterns to identify at-risk segments",
            "identify behavioral patterns in customer complaints to address systemic issues",
            "analyze customer retention metrics to identify at-risk cohorts",
            "identify cross-sell opportunities through customer purchase pattern analysis",
        ],
        "context_template": "{company} is experiencing issues and needs you to {problem}. Provide comprehensive analysis identifying root causes, affected segments, and recommend solutions.",
        "roles": ["Data Analytics Consultant", "Business Analyst", "Product Analytics"],
        "tools_pool": ["Python", "SQL", "Tableau", "Looker", "Excel"],
        "deliverables": [
            DeliverableSpec(
                name="Customer Segmentation Report",
                description="Behavioral segments with metrics and profiles",
                file_types=[".xlsx", ".pdf"],
                sheets=[
                    SheetRule(name="Segments", required_columns=["Segment", "Count", "Revenue", "Churn Rate", "Satisfaction Score"]),
                    SheetRule(name="Metrics", required_columns=["Metric", "Current Value", "Benchmark", "Variance", "Trend"]),
                ],
                calc_rules=[],
            ),
            DeliverableSpec(
                name="Churn Analysis Dashboard",
                description="Identify high-risk segments and churn predictors",
                file_types=[".xlsx", ".pdf"],
                sheets=[
                    SheetRule(name="Anomalies", required_columns=["Type", "Severity", "Detected Date", "Description", "Impact"]),
                ],
                calc_rules=[],
            ),
            DeliverableSpec(
                name="Recommendations & Action Plan",
                description="Prioritized recommendations to improve retention",
                file_types=[".pdf", ".docx"],
                sheets=[],
                calc_rules=[],
            ),
        ],
        "rubric": {"problem_identification": 25, "root_cause_analysis": 30, "data_quality": 20, "recommendations": 25},
    },

    # ---- Performance Metrics / Product Engagement -------------------------
    "performance_metrics": {
        "title_templates": [
            "Product Performance Metrics and Anomaly Detection for {company}",
            "User Engagement Drop Root-Cause Analysis for {company}",
            "Product Feature Adoption and Retention Analysis for {company}",
        ],
        "problems": [
            "find root causes of declining user engagement across product features",
            "analyze website traffic to discover why conversion rate is declining",
        ],
        "context_template": "{company} SaaS product is experiencing unexpected performance dips. Need root cause analysis: {problem}.",
        "roles": ["Product Analytics Engineer", "Data Analyst", "Analytics Engineer"],
        "tools_pool": ["Python", "SQL", "Grafana", "Amplitude", "Mixpanel"],
        "deliverables": [
            DeliverableSpec(
                name="Performance Analysis Report",
                description="Trend analysis and anomaly detection results",
                file_types=[".pdf", ".xlsx"],
                sheets=[
                    SheetRule(name="Metrics", required_columns=["Metric", "Current Value", "Benchmark", "Variance", "Trend"]),
                    SheetRule(name="Trends", required_columns=["Day", "DAU", "Session Length", "Churn"]),
                ],
                calc_rules=[],
            ),
            DeliverableSpec(
                name="Feature Breakdown",
                description="Per-feature adoption, drop-off, and satisfaction",
                file_types=[".xlsx"],
                sheets=[
                    SheetRule(name="Features", required_columns=["Feature", "Adoption Rate", "Avg Sessions", "Drop-off Rate", "Satisfaction"]),
                ],
                calc_rules=[],
            ),
            DeliverableSpec(
                name="Root Cause Findings",
                description="Detailed findings and recommendations",
                file_types=[".docx", ".pdf"],
                sheets=[],
                calc_rules=[],
            ),
        ],
        "rubric": {"problem_identification": 30, "root_cause_analysis": 25, "data_quality": 20, "recommendations": 25},
    },

    # ---- API Performance --------------------------------------------------
    "api_performance": {
        "title_templates": [
            "API Performance Investigation for {company}",
            "Request/Response Time and Error Rate Analysis for {company}",
            "Backend Reliability and Latency Root-Cause Analysis for {company}",
        ],
        "problems": [
            "identify performance bottlenecks in application by analyzing system logs",
            "investigate API performance issues through request/response time analysis",
        ],
        "context_template": "{company} is experiencing API performance degradation impacting user experience. Need to {problem}.",
        "roles": ["Backend Performance Engineer", "Data Analyst", "Analytics Engineer"],
        "tools_pool": ["Python", "SQL", "Datadog", "Grafana"],
        "deliverables": [
            DeliverableSpec(
                name="API Performance Analysis Report",
                description="Endpoint-level response time, latency distribution, and throughput trends",
                file_types=[".pdf", ".xlsx"],
                sheets=[
                    SheetRule(name="Endpoint Metrics", required_columns=["Endpoint", "Avg Response Time (ms)", "P95 Latency", "P99 Latency", "Error Rate %", "Throughput (req/s)"]),
                    SheetRule(name="Time Series", required_columns=["Day", "Response Time", "Error Rate", "Request Count"]),
                ],
                calc_rules=["Response time percentiles calculated from request logs", "Error rate = total errors / total requests"],
            ),
            DeliverableSpec(
                name="Root Cause Analysis",
                description="Identified bottlenecks, affected endpoints, and service dependencies",
                file_types=[".docx", ".pdf"],
                sheets=[],
                calc_rules=[],
            ),
            DeliverableSpec(
                name="Performance Optimization Roadmap",
                description="Prioritized recommendations with implementation effort and expected impact",
                file_types=[".docx", ".xlsx"],
                sheets=[],
                calc_rules=[],
            ),
        ],
        "rubric": {"problem_identification": 30, "root_cause_analysis": 25, "data_quality": 20, "recommendations": 25},
    },

    # ---- Marketing Funnel / Attribution -----------------------------------
    "marketing_funnel": {
        "title_templates": [
            "Marketing Funnel Attribution and Cohort Performance for {company}",
            "CAC/LTV and Channel ROI Analysis for {company}",
            "Paid vs Organic Performance Deep Dive for {company}",
        ],
        "problems": [
            "analyze sales pipeline data to find why deals are stalling at proposal stage",
            "analyze customer segmentation to optimize marketing spend allocation",
            "identify seasonal patterns affecting demand forecasting accuracy",
        ],
        "context_template": "{company} wants clear channel attribution and cohort retention. Specifically, needs to {problem}.",
        "roles": ["Marketing Data Analyst", "Business Analyst", "Data Analyst"],
        "tools_pool": ["SQL", "Python", "Looker", "Google Analytics", "Excel"],
        "deliverables": [
            DeliverableSpec(
                name="Attribution and Cohort Report",
                description="Channel attribution, CAC/LTV, and cohort retention by channel",
                file_types=[".xlsx", ".pdf"],
                sheets=[
                    SheetRule(name="Metrics", required_columns=["Metric", "Current Value", "Benchmark", "Variance", "Trend"]),
                    SheetRule(name="Segments", required_columns=["Channel", "Count", "Revenue", "Churn Rate", "Satisfaction Score"]),
                ],
                calc_rules=[],
            ),
            DeliverableSpec(
                name="Experiment Readout",
                description="A/B test results with lift, confidence, and next steps",
                file_types=[".pdf", ".docx"],
                sheets=[],
                calc_rules=[],
            ),
        ],
        "rubric": {"problem_identification": 25, "root_cause_analysis": 30, "data_quality": 20, "recommendations": 25},
    },

    # ---- Marketing Attribution Quality ------------------------------------
    "marketing_attribution": {
        "title_templates": [
            "Marketing Attribution Quality and Data Accuracy Analysis for {company}",
            "Channel Attribution Reconciliation and UTM Audit for {company}",
        ],
        "problems": [
            "detect data quality issues impacting marketing attribution accuracy",
            "identify marketing campaign underperformance through attribution analysis",
        ],
        "context_template": "{company} has conflicting channel data. Need to {problem}.",
        "roles": ["Marketing Data Analyst", "Data Analyst", "Analytics Engineer"],
        "tools_pool": ["SQL", "Python", "Google Analytics", "Looker", "Excel"],
        "deliverables": [
            DeliverableSpec(
                name="Attribution Model Comparison",
                description="Channel credit by attribution model with variance analysis",
                file_types=[".xlsx", ".pdf"],
                sheets=[
                    SheetRule(name="Models", required_columns=["Channel", "First-Touch", "Last-Touch", "Linear", "Variance"]),
                ],
                calc_rules=[],
            ),
            DeliverableSpec(
                name="UTM Tracking Audit",
                description="Identified tracking gaps and unattributed traffic analysis",
                file_types=[".xlsx"],
                sheets=[
                    SheetRule(name="Issues", required_columns=["Issue", "Severity", "Affected Traffic %", "Source", "Impact"]),
                ],
                calc_rules=[],
            ),
            DeliverableSpec(
                name="Recommendations & Roadmap",
                description="Prioritized fixes for attribution accuracy",
                file_types=[".pdf", ".docx"],
                sheets=[],
                calc_rules=[],
            ),
        ],
        "rubric": {"problem_identification": 30, "root_cause_analysis": 25, "data_quality": 25, "recommendations": 20},
    },

    # ---- Ops / SLA --------------------------------------------------------
    "ops_sla": {
        "title_templates": [
            "Operations SLA, Quality, and Cycle Time Analysis for {company}",
            "Support Queue Backlog and SLA Compliance Review for {company}",
            "Operational Efficiency and Quality Metrics Analysis for {company}",
        ],
        "problems": [
            "investigate operational inefficiencies causing 40% increase in support ticket resolution time",
            "investigate supplier performance issues affecting delivery times",
            "investigate quality control failures in manufacturing process",
            "analyze delivery logistics data to find route optimization opportunities",
        ],
        "context_template": "{company} customer support org needs SLA compliance and backlog analysis. Specifically: {problem}.",
        "roles": ["Operations Data Analyst", "Business Analyst", "Operations Analyst"],
        "tools_pool": ["SQL", "Python", "Tableau", "Excel"],
        "deliverables": [
            DeliverableSpec(
                name="SLA and Backlog Dashboard",
                description="SLA attainment, backlog aging, and cycle time by queue/region",
                file_types=[".xlsx", ".pdf"],
                sheets=[
                    SheetRule(name="Metrics", required_columns=["Metric", "Current Value", "Benchmark", "Variance", "Trend"]),
                    SheetRule(name="Regions", required_columns=["Region", "Count", "Revenue", "Churn Rate", "Satisfaction Score"]),
                ],
                calc_rules=[],
            ),
            DeliverableSpec(
                name="Quality and Root Cause Report",
                description="QA scores, re-open rates, and top drivers of misses",
                file_types=[".docx", ".pdf"],
                sheets=[],
                calc_rules=[],
            ),
        ],
        "rubric": {"problem_identification": 25, "root_cause_analysis": 30, "data_quality": 20, "recommendations": 25},
    },

    # ---- Recruitment / Hiring ---------------------------------------------
    "recruitment": {
        "title_templates": [
            "Recruitment Pipeline Bottleneck Analysis for {company}",
            "Hiring Funnel and Time-to-Hire Investigation for {company}",
            "Talent Acquisition Efficiency Review for {company}",
        ],
        "problems": [
            "analyze hiring data to identify bottlenecks in recruitment process",
            "analyze employee turnover data to identify retention risks",
            "analyze employee productivity data to find efficiency gaps by team",
        ],
        "context_template": "{company} needs to {problem}. Analyze the recruitment pipeline end-to-end.",
        "roles": ["Business Analyst", "Operations Analyst", "Data Analyst"],
        "tools_pool": ["SQL", "Python", "Excel", "Tableau", "Google Sheets"],
        "deliverables": [
            DeliverableSpec(
                name="Recruitment Funnel Analysis",
                description="Stage-by-stage conversion and drop-off rates",
                file_types=[".xlsx", ".pdf"],
                sheets=[
                    SheetRule(name="Funnel", required_columns=["Stage", "Count", "Conversion Rate", "Drop-off Rate"]),
                    SheetRule(name="Sources", required_columns=["Source", "Applications", "Offers Extended", "Offers Accepted", "Quality Score"]),
                ],
                calc_rules=[],
            ),
            DeliverableSpec(
                name="Time-to-Hire Report",
                description="Hiring velocity by role with bottleneck identification",
                file_types=[".xlsx"],
                sheets=[
                    SheetRule(name="By Role", required_columns=["Role", "Avg Days to Hire", "Screen to Offer Days", "Current Openings"]),
                ],
                calc_rules=[],
            ),
            DeliverableSpec(
                name="Bottleneck Findings & Recommendations",
                description="Root causes and prioritized improvements",
                file_types=[".pdf", ".docx"],
                sheets=[],
                calc_rules=[],
            ),
        ],
        "rubric": {"problem_identification": 30, "root_cause_analysis": 25, "data_quality": 20, "recommendations": 25},
    },

    # ---- Data Quality / Metric Inconsistency ------------------------------
    "data_quality": {
        "title_templates": [
            "Cross-Department Data Quality and Metric Consistency Analysis for {company}",
            "Data Reconciliation and Source-System Alignment for {company}",
            "Reporting Accuracy and Data Pipeline Review for {company}",
        ],
        "problems": [
            "investigate inconsistencies in reported metrics across different departments",
            "identify gaps in data collection impacting business intelligence reporting",
            "investigate data inconsistencies between CRM and accounting systems",
        ],
        "context_template": "{company} departments report conflicting metrics. Need to {problem}.",
        "roles": ["Data Analyst", "Analytics Engineer", "Business Analyst"],
        "tools_pool": ["SQL", "Python", "Excel", "Google Analytics", "Amplitude"],
        "deliverables": [
            DeliverableSpec(
                name="Data Quality Assessment",
                description="Analysis of data completeness, accuracy, and consistency across departments",
                file_types=[".xlsx", ".pdf"],
                sheets=[
                    SheetRule(name="Metrics", required_columns=["Metric", "Department", "Reported Value", "Consensus Value", "Variance"]),
                    SheetRule(name="Sources", required_columns=["System", "Departments Using", "Last Sync", "Discrepancy %"]),
                ],
                calc_rules=[],
            ),
            DeliverableSpec(
                name="Root Cause Analysis",
                description="Identified causes of metric discrepancies",
                file_types=[".pdf", ".docx"],
                sheets=[],
                calc_rules=[],
            ),
            DeliverableSpec(
                name="Standardization Recommendations",
                description="Action plan for single source of truth",
                file_types=[".pdf", ".docx"],
                sheets=[],
                calc_rules=[],
            ),
        ],
        "rubric": {"problem_identification": 30, "root_cause_analysis": 20, "data_quality": 25, "recommendations": 25},
    },

    # ---- Social Sentiment / Brand Health ---------------------------------
    "social_sentiment": {
        "title_templates": [
            "Social Media Sentiment and Brand Health Analysis for {company}",
            "Brand Perception and Social Listening Report for {company}",
        ],
        "problems": [
            "analyze social media sentiment to track brand health trends",
        ],
        "context_template": "{company} needs to {problem}. Analyse cross-platform sentiment and share of voice.",
        "roles": ["Marketing Data Analyst", "Data Analyst", "Business Analyst"],
        "tools_pool": ["Python", "SQL", "Tableau", "Excel", "Google Analytics"],
        "deliverables": [
            DeliverableSpec(
                name="Sentiment Analysis Report",
                description="Platform-by-platform sentiment scores and trends",
                file_types=[".xlsx", ".pdf"],
                sheets=[
                    SheetRule(name="By Platform", required_columns=["Platform", "Mentions", "Positive %", "Negative %", "Sentiment Score"]),
                    SheetRule(name="Trends", required_columns=["Day", "Mentions", "Sentiment Score"]),
                ],
                calc_rules=[],
            ),
            DeliverableSpec(
                name="Share of Voice & Competitive Report",
                description="Brand vs competitors mention volume and sentiment",
                file_types=[".xlsx", ".pdf"],
                sheets=[],
                calc_rules=[],
            ),
            DeliverableSpec(
                name="Crisis & Opportunity Briefing",
                description="Flagged risks and positive momentum to leverage",
                file_types=[".pdf", ".docx"],
                sheets=[],
                calc_rules=[],
            ),
        ],
        "rubric": {"problem_identification": 25, "root_cause_analysis": 25, "data_quality": 25, "recommendations": 25},
    },

    # ---- Mobile App Behavior / Feature Discovery -------------------------
    "mobile_app_behavior": {
        "title_templates": [
            "Mobile App User Behavior and Feature Discoverability Analysis for {company}",
            "App Engagement and Feature Adoption Deep Dive for {company}",
        ],
        "problems": [
            "analyze mobile app user behavior to improve feature discoverability",
        ],
        "context_template": "{company} mobile app has low feature adoption. Need to {problem}.",
        "roles": ["Product Analytics", "Data Analyst", "Data Scientist"],
        "tools_pool": ["Python", "SQL", "Amplitude", "Mixpanel", "Excel"],
        "deliverables": [
            DeliverableSpec(
                name="Feature Discovery Report",
                description="Feature-level discovery, adoption, and retention rates",
                file_types=[".xlsx", ".pdf"],
                sheets=[
                    SheetRule(name="Features", required_columns=["Feature", "Discovery Rate %", "Adoption Rate %", "Retention Rate %", "DAU"]),
                    SheetRule(name="Funnel", required_columns=["Stage", "Users", "% of Total", "Drop-off Rate"]),
                ],
                calc_rules=[],
            ),
            DeliverableSpec(
                name="User Segmentation Analysis",
                description="Behavioral segments with engagement profiles",
                file_types=[".xlsx"],
                sheets=[
                    SheetRule(name="Segments", required_columns=["Segment", "Size", "Features Used", "Session Length", "Churn Risk"]),
                ],
                calc_rules=[],
            ),
            DeliverableSpec(
                name="Discoverability Improvement Plan",
                description="Prioritized UX recommendations to improve feature adoption",
                file_types=[".pdf", ".docx"],
                sheets=[],
                calc_rules=[],
            ),
        ],
        "rubric": {"problem_identification": 25, "root_cause_analysis": 30, "data_quality": 20, "recommendations": 25},
    },

    # ---- Feature Adoption Gaps -------------------------------------------
    "feature_adoption": {
        "title_templates": [
            "Feature Adoption Gap and Usage Pattern Analysis for {company}",
            "Product Stickiness and Activation Funnel Study for {company}",
        ],
        "problems": [
            "identify patterns in product usage that reveal feature adoption gaps",
        ],
        "context_template": "{company} sees users activating but not retaining. Need to {problem}.",
        "roles": ["Product Analytics", "Data Analyst", "Analytics Engineer"],
        "tools_pool": ["Python", "SQL", "Amplitude", "Mixpanel", "Tableau"],
        "deliverables": [
            DeliverableSpec(
                name="Feature Usage Report",
                description="DAU/WAU/MAU, activation rates, and adoption gaps per feature",
                file_types=[".xlsx", ".pdf"],
                sheets=[
                    SheetRule(name="Usage", required_columns=["Feature", "DAU", "WAU", "MAU", "Activation Rate", "Adoption Gap"]),
                ],
                calc_rules=[],
            ),
            DeliverableSpec(
                name="Activation Funnel Analysis",
                description="Step-by-step conversion from signup to repeat usage",
                file_types=[".xlsx"],
                sheets=[
                    SheetRule(name="Funnel", required_columns=["Step", "Conversion", "Drop-off"]),
                ],
                calc_rules=[],
            ),
            DeliverableSpec(
                name="Retention & Recommendations",
                description="Cohort retention and actionable improvements",
                file_types=[".pdf", ".docx"],
                sheets=[],
                calc_rules=[],
            ),
        ],
        "rubric": {"problem_identification": 30, "root_cause_analysis": 25, "data_quality": 20, "recommendations": 25},
    },

    # ---- Fraud Detection -------------------------------------------------
    "fraud_detection": {
        "title_templates": [
            "Fraud Pattern Detection and Transaction Risk Analysis for {company}",
            "Payment Fraud and Chargeback Root-Cause Investigation for {company}",
        ],
        "problems": [
            "detect fraud patterns in transaction data across multiple channels",
            "detect anomalies in financial transactions indicating control weaknesses",
        ],
        "context_template": "{company} is seeing rising chargebacks and suspicious transactions. Need to {problem}.",
        "roles": ["Data Analyst", "Data Scientist", "Operations Analyst"],
        "tools_pool": ["Python", "SQL", "Excel", "Tableau", "Power BI"],
        "deliverables": [
            DeliverableSpec(
                name="Fraud Pattern Report",
                description="Channel and payment-method fraud analysis",
                file_types=[".xlsx", ".pdf"],
                sheets=[
                    SheetRule(name="Channels", required_columns=["Channel", "Volume", "Fraud Rate", "Anomaly Rate", "Avg Risk Score"]),
                    SheetRule(name="Methods", required_columns=["Payment Method", "Volume", "Fraud Rate"]),
                ],
                calc_rules=[],
            ),
            DeliverableSpec(
                name="Anomaly & Risk Assessment",
                description="Flagged patterns with evidence and risk level",
                file_types=[".pdf", ".docx"],
                sheets=[],
                calc_rules=[],
            ),
            DeliverableSpec(
                name="Mitigation Recommendations",
                description="Prioritized controls and rule changes",
                file_types=[".pdf", ".docx"],
                sheets=[],
                calc_rules=[],
            ),
        ],
        "rubric": {"problem_identification": 30, "root_cause_analysis": 25, "data_quality": 20, "recommendations": 25},
    },
}


# ---------------------------------------------------------------------------
# Company types shared across profiles
# ---------------------------------------------------------------------------

COMPANY_TYPES = [
    "SaaS startup", "E-commerce business", "Digital agency", "Consulting firm",
    "Marketplace platform", "B2B service provider", "Fintech company",
    "Logistics startup", "Healthcare provider", "Real estate firm",
    "Manufacturing company", "Subscription box service", "Staffing agency",
    "Software development shop", "Mobile app studio", "Nonprofit organization",
    "Recruitment firm", "Marketing agency", "Accounting practice",
    "Insurance brokerage", "EdTech platform", "Travel & hospitality",
    "Cybersecurity firm", "AI/ML startup", "Biotech company",
    "Sustainability company", "Fashion & retail", "Food & beverage",
    "Automotive supplier", "Construction firm",
]

URGENCY_OPTIONS = ["normal", "high", "urgent"]
DEADLINE_HOURS = [48, 60, 72, 96]


# ---------------------------------------------------------------------------
# Objective templates
# ---------------------------------------------------------------------------

FINANCIAL_OBJECTIVES_TEMPLATES = [
    {
        "title": "Data Validation & Reconciliation",
        "description": "Ensure all source data is complete, accurate, and reconciles to control totals",
        "success_criteria": [
            "All transactions reconcile to source systems",
            "No missing or duplicate records",
            "All discrepancies documented and explained",
        ],
    },
    {
        "title": "Analysis & Insight Generation",
        "description": "Perform detailed analysis to uncover key trends, outliers, and business insights",
        "success_criteria": [
            "Identified top 5 drivers of variance or change",
            "Month-over-month and year-over-year trends analyzed",
            "Outliers and anomalies documented with explanations",
        ],
    },
    {
        "title": "Executive Summary Creation",
        "description": "Develop clear, concise summary communicating key findings to stakeholders",
        "success_criteria": [
            "1-page executive summary with key metrics highlighted",
            "Top 3 recommendations provided",
            "Impact quantified in business terms",
        ],
    },
    {
        "title": "Documentation & Support",
        "description": "Prepare comprehensive documentation explaining methodology and calculations",
        "success_criteria": [
            "Calculation logic clearly documented",
            "Data dictionary provided for all metrics",
            "Assumptions and limitations outlined",
        ],
    },
    {
        "title": "Stakeholder Communication",
        "description": "Present findings and recommendations in a clear, actionable manner",
        "success_criteria": [
            "Key findings explained in business context",
            "Recommended actions with expected outcomes",
            "Timeline for implementation provided",
        ],
    },
]

DATA_ANALYSIS_OBJECTIVES_TEMPLATES = [
    {
        "title": "Problem Diagnosis",
        "description": "Clearly identify and document the specific problem, its scope, and impact",
        "success_criteria": [
            "Problem statement is measurable and specific",
            "Affected customer/user segments identified",
            "Business impact quantified with current metrics",
        ],
    },
    {
        "title": "Root Cause Analysis",
        "description": "Investigate underlying causes using data-driven evidence",
        "success_criteria": [
            "Multiple hypotheses tested with data",
            "Root causes prioritized by impact",
            "Correlation vs causation clearly distinguished",
        ],
    },
    {
        "title": "Data Quality Assessment",
        "description": "Evaluate data completeness, accuracy, and consistency issues",
        "success_criteria": [
            "Data quality issues identified and quantified",
            "Impact on analysis documented",
            "Data limitations acknowledged",
        ],
    },
    {
        "title": "Recommendations Development",
        "description": "Create specific, actionable recommendations to address identified issues",
        "success_criteria": [
            "3-5 prioritized recommendations with business case",
            "Expected impact quantified for each recommendation",
            "Implementation considerations outlined",
        ],
    },
    {
        "title": "Results Presentation",
        "description": "Present analysis in clear, visual format for stakeholder consumption",
        "success_criteria": [
            "Key findings presented visually with charts/dashboards",
            "Executive summary with key metrics highlighted",
            "Recommendations ranked by effort vs impact",
        ],
    },
]


# ---------------------------------------------------------------------------
# Generic objective generators (used by sample-cases / legacy paths)
# ---------------------------------------------------------------------------

def _generate_financial_objectives() -> List[ObjectiveSpec]:
    """Generate 3-4 generic objectives for a financial VA case."""
    num = random.randint(3, 4)
    selected = random.sample(FINANCIAL_OBJECTIVES_TEMPLATES, min(num, len(FINANCIAL_OBJECTIVES_TEMPLATES)))
    return [ObjectiveSpec(title=t["title"], description=t["description"], success_criteria=t["success_criteria"]) for t in selected]


def _generate_data_analysis_objectives() -> List[ObjectiveSpec]:
    """Generate 3-4 generic objectives for a data analysis case."""
    num = random.randint(3, 4)
    selected = random.sample(DATA_ANALYSIS_OBJECTIVES_TEMPLATES, min(num, len(DATA_ANALYSIS_OBJECTIVES_TEMPLATES)))
    return [ObjectiveSpec(title=t["title"], description=t["description"], success_criteria=t["success_criteria"]) for t in selected]


# ---------------------------------------------------------------------------
# Contextual objective generators
# ---------------------------------------------------------------------------

def _generate_financial_objectives_contextual(case: "Case") -> List[ObjectiveSpec]:
    """Generate context-aware objectives for a financial VA case."""
    objectives = []
    company_type = case.title.split(" for ")[-1] if " for " in case.title else "your company"
    metric = case.title.split(" ")[0] if " " in case.title else "financial data"
    deliverable_names = [d.name for d in case.deliverables]
    tools_str = ", ".join(case.tools) if case.tools else "available tools"

    objectives.append(ObjectiveSpec(
        title="Data Collection & Validation",
        description=f"Gather and validate {metric.lower()} data for {company_type} from relevant source systems.",
        success_criteria=[
            f"All {metric.lower()} data extracted and reconciled to control totals",
            "Missing or incomplete records identified and documented",
            "Data quality issues logged with root cause analysis",
            "Variance explanations documented for any discrepancies found",
        ],
    ))

    if any("Report" in d or "Analysis" in d for d in deliverable_names):
        analysis_deliverables = [d for d in deliverable_names if "Analysis" in d or "Report" in d]
        objectives.append(ObjectiveSpec(
            title="Comprehensive Analysis & Breakdown",
            description=f"Perform detailed {metric.lower()} analysis for {company_type} using {tools_str}. Create: {', '.join(analysis_deliverables[:2])}.",
            success_criteria=[
                f"Month-over-month and year-over-year {metric.lower()} trends analyzed",
                "Top 5 drivers of variance identified with quantified impact",
                "Seasonal patterns, outliers, and anomalies documented",
                "Analysis methodology clearly documented",
            ],
        ))

    if any("Reconciliation" in d or "Variance" in d for d in deliverable_names):
        objectives.append(ObjectiveSpec(
            title="Reconciliation & Variance Analysis",
            description=f"Reconcile {metric.lower()} figures across all source systems and prepare variance analysis.",
            success_criteria=[
                "Line-by-line reconciliation completed with 100% balance achieved",
                "All variance explanations supported by documentation",
                f"Variance analysis shows impact on {company_type} financial position",
                "Reconciliation schedule updated for stakeholder review",
            ],
        ))

    if any("Brief" in d or "Summary" in d for d in deliverable_names):
        objectives.append(ObjectiveSpec(
            title="Executive Summary & Recommendations",
            description=f"Develop executive summary communicating {metric.lower()} findings to {company_type} stakeholders.",
            success_criteria=[
                "1-page executive summary with key metrics highlighted",
                "Top 3 recommendations with business case and expected impact",
                "Actions prioritized by effort vs. impact",
                "Implementation timeline and resource requirements outlined",
            ],
        ))

    return objectives[:4]


def _generate_data_analysis_objectives_contextual(case: "Case") -> List[ObjectiveSpec]:
    """Generate context-aware objectives for a data analysis case."""
    objectives = []
    company_type = case.title.split(" for ")[-1] if " for " in case.title else "the organization"
    problem_phrase = case.context.split("needs you to ")[-1].split(".")[0] if "needs you to" in case.context else "address the identified issues"
    deliverable_names = [d.name for d in case.deliverables]
    tools_str = ", ".join(case.tools) if case.tools else "analytical tools"

    objectives.append(ObjectiveSpec(
        title="Problem Identification & Scoping",
        description=f"Clearly define the business problem for {company_type}: {problem_phrase}.",
        success_criteria=[
            f"Problem statement for {company_type} is specific and measurable",
            "Affected customer segments or business areas quantified",
            "Business impact in terms of revenue, cost, or efficiency losses calculated",
            "Scope boundaries clearly defined",
        ],
    ))

    if any("Root Cause" in d or "Diagnosis" in d for d in deliverable_names):
        objectives.append(ObjectiveSpec(
            title="Root Cause Analysis",
            description=f"Investigate underlying causes using {tools_str}.",
            success_criteria=[
                f"3-5 root causes identified for {problem_phrase} with data evidence",
                "Each root cause validated with at least 2 data sources",
                "Root causes ranked by business impact",
                "Correlation vs. causation clearly distinguished",
            ],
        ))

    if any("Quality" in d or "Anomaly" in d for d in deliverable_names):
        objectives.append(ObjectiveSpec(
            title="Data Quality Assessment & Anomaly Detection",
            description=f"Evaluate data completeness and consistency for {company_type}.",
            success_criteria=[
                "Data quality issues quantified by severity",
                "Impact on analysis and business decisions documented",
                "Anomalies and outliers identified with explanations",
                "Data limitations acknowledged",
            ],
        ))

    if any("Recommendation" in d or "Action" in d or "Roadmap" in d or "Plan" in d for d in deliverable_names):
        objectives.append(ObjectiveSpec(
            title="Recommendations & Action Plan",
            description=f"Develop 3-5 prioritized recommendations for {company_type}.",
            success_criteria=[
                f"3-5 recommendations to address {problem_phrase}",
                "Expected impact quantified for each recommendation",
                "Implementation effort and resource requirements estimated",
                "Quick wins identified and ranked by effort vs. impact",
            ],
        ))

    return objectives[:4]


# ---------------------------------------------------------------------------
# CASE GENERATORS
# ---------------------------------------------------------------------------

def generate_random_case() -> "Case":
    """Generate a random practice case - either financial VA or data analysis (50/50)."""
    if random.choice([True, False]):
        return _generate_financial_case()
    else:
        return generate_data_analysis_case()


def _generate_financial_case() -> "Case":
    """Generate a unique, realistic financial VA practice case."""

    case_id = f"case-{datetime.now().strftime('%Y%m%d%H%M%S')}-{random.randint(1000, 9999)}"
    company_type = random.choice(COMPANY_TYPES)

    # Pick a random financial profile – guarantees coherent (title, context, deliverables, data)
    profile_key = random.choice(list(FINANCIAL_PROFILES.keys()))
    profile = FINANCIAL_PROFILES[profile_key]

    title = random.choice(profile["title_templates"]).format(company=company_type)
    need = random.choice(profile["needs"])
    context = profile["context_template"].format(company=company_type.capitalize(), need=need)
    role = random.choice(profile["roles"])

    num_tools = random.randint(2, min(3, len(profile["tools_pool"])))
    tools = random.sample(profile["tools_pool"], num_tools)

    urgency = random.choice(URGENCY_OPTIONS)
    deadline_hours = random.choice(DEADLINE_HOURS)

    deliverables = list(profile["deliverables"])

    return Case(
        id=case_id,
        version="v1",
        title=title,
        context=context,
        role=role,
        case_type="financial",
        data_profile=profile_key,
        tools=tools,
        deadline_hours=deadline_hours,
        urgency=urgency,
        deliverables=deliverables,
        objectives=_generate_financial_objectives(),
        rubric=profile["rubric"],
    )


def generate_data_analysis_case() -> "Case":
    """Generate a unique, realistic data analysis case."""

    case_id = f"case-{datetime.now().strftime('%Y%m%d%H%M%S')}-{random.randint(1000, 9999)}"
    company_type = random.choice(COMPANY_TYPES)

    profile_key = random.choice(list(DATA_ANALYSIS_PROFILES.keys()))
    profile = DATA_ANALYSIS_PROFILES[profile_key]

    title = random.choice(profile["title_templates"]).format(company=company_type)
    problem = random.choice(profile["problems"])
    context = profile["context_template"].format(company=company_type.capitalize(), problem=problem)
    role = random.choice(profile["roles"])

    num_tools = random.randint(2, min(3, len(profile["tools_pool"])))
    tools = random.sample(profile["tools_pool"], num_tools)

    urgency = random.choice(URGENCY_OPTIONS)
    deadline_hours = random.choice(DEADLINE_HOURS)

    deliverables = list(profile["deliverables"])

    return Case(
        id=case_id,
        version="v1",
        title=title,
        context=context,
        role=role,
        case_type="analysis",
        data_profile=profile_key,
        tools=tools,
        deadline_hours=deadline_hours,
        urgency=urgency,
        deliverables=deliverables,
        objectives=_generate_data_analysis_objectives(),
        rubric=profile["rubric"],
    )


def calculate_case_generation_capacity() -> dict:
    """Calculate theoretical maximum unique cases that can be generated."""
    from math import comb

    company_types = len(COMPANY_TYPES)

    fin_profiles = len(FINANCIAL_PROFILES)
    fin_needs_total = sum(len(p["needs"]) for p in FINANCIAL_PROFILES.values())
    fin_titles_total = sum(len(p["title_templates"]) for p in FINANCIAL_PROFILES.values())
    fin_tool_combos = sum(
        sum(comb(len(p["tools_pool"]), k) for k in range(2, min(4, len(p["tools_pool"])) + 1))
        for p in FINANCIAL_PROFILES.values()
    )

    financial_combos = (
        company_types
        * fin_needs_total
        * fin_titles_total
        * fin_tool_combos
        * len(URGENCY_OPTIONS)
        * len(DEADLINE_HOURS)
    )

    ana_profiles = len(DATA_ANALYSIS_PROFILES)
    ana_problems_total = sum(len(p["problems"]) for p in DATA_ANALYSIS_PROFILES.values())
    ana_titles_total = sum(len(p["title_templates"]) for p in DATA_ANALYSIS_PROFILES.values())
    ana_tool_combos = sum(
        sum(comb(len(p["tools_pool"]), k) for k in range(2, min(4, len(p["tools_pool"])) + 1))
        for p in DATA_ANALYSIS_PROFILES.values()
    )

    analysis_combos = (
        company_types
        * ana_problems_total
        * ana_titles_total
        * ana_tool_combos
        * len(URGENCY_OPTIONS)
        * len(DEADLINE_HOURS)
    )

    total = financial_combos + analysis_combos

    return {
        "financial_cases": {
            "profiles": fin_profiles,
            "company_types": company_types,
            "total_needs": fin_needs_total,
            "title_templates": fin_titles_total,
            "tool_combinations": fin_tool_combos,
            "urgency_levels": len(URGENCY_OPTIONS),
            "deadline_options": len(DEADLINE_HOURS),
            "unique_combinations": int(financial_combos),
        },
        "data_analysis_cases": {
            "profiles": ana_profiles,
            "company_types": company_types,
            "total_problems": ana_problems_total,
            "title_templates": ana_titles_total,
            "tool_combinations": ana_tool_combos,
            "urgency_levels": len(URGENCY_OPTIONS),
            "deadline_options": len(DEADLINE_HOURS),
            "unique_combinations": int(analysis_combos),
        },
        "total_unique_cases": int(total),
        "timestamp_variation": "Additional uniqueness from millisecond-precision timestamps",
    }
