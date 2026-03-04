import random
from datetime import datetime, timedelta
from app.schemas.cases import Case


def generate_mock_data(case: Case) -> dict:
    """
    Generate mock/sample data based on the case's data_profile.

    Dispatch priority:
      1. Explicit ``case.data_profile`` (set by the generator) — guaranteed match.
      2. Legacy hard-coded case-id checks (for the 9 sample cases).
      3. Keyword matching on title/context (kept only as a safety-net for
         externally-constructed Case objects that lack a profile).
      4. Fallback by ``case_type``.
    """

    # ---- 1. Profile-based dispatch (primary path) -------------------------
    _PROFILE_GENERATORS = {
        # Financial profiles
        "cashflow": _generate_monthly_cashflow_data,
        "expense_audit": _generate_expense_audit_data,
        "revenue_forecast": _generate_revenue_forecast_data,
        "payroll": _generate_payroll_data,
        "profitability": _generate_monthly_cashflow_data,   # reuses cashflow shape (P&L-like)
        "reconciliation": _generate_financial_mock_data,     # general ledger reconciliation
        # Analysis profiles
        "customer_analytics": _generate_customer_analytics_data,
        "performance_metrics": _generate_performance_metrics_data,
        "api_performance": _generate_api_performance_nonprofit_data,
        "marketing_funnel": _generate_marketing_funnel_data,
        "marketing_attribution": _generate_marketing_attribution_quality_data,
        "ops_sla": _generate_ops_sla_data,
        "recruitment": _generate_recruitment_analysis_data,
        "data_quality": _generate_data_quality_analysis_data,
        "social_sentiment": _generate_social_sentiment_analysis_data,
        "mobile_app_behavior": _generate_mobile_app_behavior_data,
        "feature_adoption": _generate_feature_adoption_gaps_data,
        "fraud_detection": _generate_fraud_detection_data,
    }

    if case.data_profile and case.data_profile in _PROFILE_GENERATORS:
        return _PROFILE_GENERATORS[case.data_profile](case)

    # ---- 2. Legacy case-id overrides (sample cases without profile) -------
    _LEGACY_ID_MAP = {
        "case-monthly-cashflow": _generate_monthly_cashflow_data,
        "case-expense-audit": _generate_expense_audit_data,
        "case-revenue-forecast": _generate_revenue_forecast_data,
        "case-payroll-reconciliation": _generate_payroll_data,
        "case-customer-analytics": _generate_customer_analytics_data,
        "case-performance-metrics": _generate_performance_metrics_data,
        "case-api-performance-nonprofit": _generate_api_performance_nonprofit_data,
        "case-marketing-funnel": _generate_marketing_funnel_data,
        "case-ops-sla-quality": _generate_ops_sla_data,
    }
    if case.id in _LEGACY_ID_MAP:
        return _LEGACY_ID_MAP[case.id](case)

    # ---- 3. Keyword fallback (safety-net) ---------------------------------
    context_lower = (case.context or "").lower()
    title_lower = (case.title or "").lower()
    text_lower = f"{title_lower} {context_lower}"

    _KEYWORD_ROUTES: list[tuple[list[str], callable]] = [
        (["cash flow", "cashflow", "runway", "ar hygiene", "receivable"], _generate_monthly_cashflow_data),
        (["expense", "budget", "variance", "audit"], _generate_expense_audit_data),
        (["revenue forecast", "mrr", "forecast", "expansion", "churn"], _generate_revenue_forecast_data),
        (["payroll", "contractor", "reconciliation", "tax compliance"], _generate_payroll_data),
        (["customer", "segmentation", "behavior", "churn predictor", "retention"], _generate_customer_analytics_data),
        (["product performance", "engagement", "feature", "anomaly", "dau"], _generate_performance_metrics_data),
        (["api", "endpoint", "request", "response time", "latency"], _generate_api_performance_nonprofit_data),
        (["attribution", "marketing attribution", "attribution accuracy"], _generate_marketing_attribution_quality_data),
        (["marketing", "funnel", "cohort", "cac", "ltv"], _generate_marketing_funnel_data),
        (["sla", "backlog", "support queue", "quality"], _generate_ops_sla_data),
        (["hiring", "recruitment", "bottleneck", "candidate"], _generate_recruitment_analysis_data),
        (["inconsistencies", "data quality", "discrepancies"], _generate_data_quality_analysis_data),
        (["social media", "sentiment", "brand health"], _generate_social_sentiment_analysis_data),
        (["mobile app", "feature discovery", "app engagement"], _generate_mobile_app_behavior_data),
        (["feature adoption", "adoption gap", "usage pattern", "product usage"], _generate_feature_adoption_gaps_data),
        (["fraud", "chargeback", "payment", "transaction risk", "dispute"], _generate_fraud_detection_data),
    ]

    for keywords, gen_fn in _KEYWORD_ROUTES:
        if any(kw in text_lower for kw in keywords):
            return gen_fn(case)

    # ---- 4. Final fallback by case_type -----------------------------------
    if case.case_type == "analysis":
        return _generate_analysis_mock_data(case)
    return _generate_financial_mock_data(case)


def _generate_monthly_cashflow_data(case: Case) -> dict:
    """
    Generate monthly cash flow data for digital agency.
    Focus on lumpy retainer revenue, AR aging, and runway calculation.
    """
    clients = ["ClientA (Retainer)", "ClientB (Project)", "ClientC (Monthly)", "ClientD (Ad-hoc)", "ClientE (Retainer)"]
    
    # Retainer-based revenue with lumpiness
    retainers = []
    for client in clients:
        base_retainer = random.randint(3000, 12000)
        invoice_frequency = random.choice(["Monthly", "Quarterly", "Bi-weekly", "Ad-hoc"])
        retainers.append({
            "client": client,
            "monthly_retainer": base_retainer,
            "frequency": invoice_frequency,
            "last_invoice_date": (datetime.now() - timedelta(days=random.randint(5, 60))).strftime("%Y-%m-%d"),
            "next_due_date": (datetime.now() + timedelta(days=random.randint(5, 45))).strftime("%Y-%m-%d"),
        })
    
    # AR aging with lumpy patterns
    ar_records = []
    for i, client in enumerate(clients):
        invoice_date = datetime.now() - timedelta(days=random.randint(10, 120))
        due_date = invoice_date + timedelta(days=30)
        days_outstanding = (datetime.now() - due_date).days
        
        ar_records.append({
            "client": client,
            "invoice_number": f"INV-{random.randint(5000, 9999)}",
            "invoice_date": invoice_date.strftime("%Y-%m-%d"),
            "due_date": due_date.strftime("%Y-%m-%d"),
            "amount": round(random.uniform(2500, 15000), 2),
            "days_outstanding": max(0, days_outstanding),
            "status": "Paid" if days_outstanding < 0 else ("Overdue" if days_outstanding > 30 else "Current"),
            "bucket": "Current" if days_outstanding <= 0 else ("1-30" if days_outstanding <= 30 else ("31-60" if days_outstanding <= 60 else "60+")),
        })
    
    # Weekly cash flow with lumpiness
    cash_flow = []
    starting_balance = 25000
    running_balance = starting_balance
    
    for week in range(12):
        # Lumpy inflows (retainer hits in certain weeks)
        if week % 4 == 0:
            inflows = round(random.uniform(20000, 35000), 2)  # Retainer week
        else:
            inflows = round(random.uniform(2000, 8000), 2)  # Light week
        
        outflows = round(random.uniform(5000, 18000), 2)
        net = inflows - outflows
        running_balance = max(0, running_balance + net)
        
        cash_flow.append({
            "week": week + 1,
            "inflows": inflows,
            "outflows": outflows,
            "net": net,
            "balance": running_balance,
            "balance_note": "Low balance - risk" if running_balance < 15000 else "Healthy"
        })
    
    # Disbursements (typical agency expenses)
    disbursements = []
    expense_types = ["Contractor", "Software SaaS", "Cloud Hosting", "Marketing", "Equipment", "Office", "Professional Services"]
    for _ in range(random.randint(12, 20)):
        disbursements.append({
            "date": (datetime.now() - timedelta(days=random.randint(5, 90))).strftime("%Y-%m-%d"),
            "vendor": random.choice(["Figma", "AWS", "Stripe", "Slack", "Asana", "ContractorCorp", "Office Space LLC"]),
            "category": random.choice(expense_types),
            "amount": round(random.uniform(500, 8000), 2),
            "status": random.choice(["Paid", "Pending", "Scheduled"])
        })
    
    return {
        "company": "Digital Agency",
        "report_date": datetime.now().strftime("%Y-%m-%d"),
        "retainers": retainers,
        "ar_records": ar_records,
        "cash_flow_weekly": cash_flow,
        "disbursements": disbursements,
        "summary": {
            "total_ar_outstanding": round(sum(r["amount"] for r in ar_records), 2),
            "ar_current": round(sum(r["amount"] for r in ar_records if r["status"] == "Current"), 2),
            "ar_overdue": round(sum(r["amount"] for r in ar_records if r["status"] == "Overdue"), 2),
            "current_cash_balance": running_balance,
            "weeks_of_runway": round(running_balance / (sum(c["outflows"] for c in cash_flow) / len(cash_flow)), 1) if cash_flow else 0,
            "at_risk_clients": len([r for r in ar_records if r["days_outstanding"] > 60]),
            "next_30_days_inflows": round(sum(r["amount"] for r in ar_records if r["bucket"] in ["Current", "1-30"]), 2),
        }
    }


def _generate_financial_mock_data(case: Case) -> dict:
    """Generate mock financial data for testing."""
    
    company_name = case.title.split(" for ")[-1] if " for " in case.title else "Test Company"
    
    # Randomize data counts
    num_transactions = random.randint(15, 40)
    num_ar_records = random.randint(5, 15)
    num_weeks = random.randint(8, 16)
    
    # Choose descriptions/categories based on case
    if case.id == "case-expense-audit":
        descriptions = ["Vendor Bill", "SaaS Subscription", "Marketing Spend", "Logistics", "Office Expense", "Travel", "Contractor Invoice"]
        categories = ["Expense", "Marketing", "Ops", "G&A", "Technology", "Payroll"]
    elif case.id == "case-payroll-reconciliation":
        descriptions = ["Salary", "Contractor Payment", "Bonus", "Payroll Tax", "Benefits", "Reimbursement"]
        categories = ["Payroll", "Tax", "Benefits", "Reimbursement"]
    elif case.id == "case-revenue-forecast":
        descriptions = ["New MRR", "Expansion", "Downgrade", "Churn", "One-time", "Usage"]
        categories = ["Revenue", "Churn", "Expansion", "One-time"]
    else:
        descriptions = ["Customer Invoice", "Service Revenue", "Product Sale", "Subscription Payment", "Refund", "Adjustment", "Fee"]
        categories = ["Revenue", "Expense", "Payroll", "Operating", "Capital"]

    # Sample transaction data
    transactions = []
    start_date = datetime.now() - timedelta(days=90)
    
    for i in range(num_transactions):
        trans_date = start_date + timedelta(days=random.randint(0, 90))
        transactions.append({
            "date": trans_date.strftime("%Y-%m-%d"),
            "description": random.choice(descriptions),
            "category": random.choice(categories),
            "amount": round(random.uniform(500, 50000), 2),
            "status": random.choice(["Received", "Pending", "Overdue"])
        })
    
    # Sample AR data
    ar_records = []
    for i in range(num_ar_records):
        invoice_date = datetime.now() - timedelta(days=random.randint(10, 120))
        due_date = invoice_date + timedelta(days=30)
        days_overdue = (datetime.now() - due_date).days
        
        ar_records.append({
            "customer": f"Customer {i+1}",
            "invoice_number": f"INV-{2024}{random.randint(1000, 9999)}",
            "invoice_date": invoice_date.strftime("%Y-%m-%d"),
            "due_date": due_date.strftime("%Y-%m-%d"),
            "amount": round(random.uniform(1000, 25000), 2),
            "days_overdue": max(0, days_overdue),
            "status": "Paid" if days_overdue < 0 else ("Overdue" if days_overdue > 0 else "Current")
        })
    
    # Sample cash flow data
    cash_flow = []
    running_balance = 50000
    for week in range(num_weeks):
        inflows = round(random.uniform(5000, 20000), 2)
        outflows = round(random.uniform(3000, 15000), 2)
        net = inflows - outflows
        running_balance += net
        
        cash_flow.append({
            "week": week + 1,
            "inflows": inflows,
            "outflows": outflows,
            "net": net,
            "balance": running_balance
        })
    
    return {
        "company": company_name,
        "report_date": datetime.now().strftime("%Y-%m-%d"),
        "transactions": transactions,
        "ar_aging": ar_records,
        "cash_flow_forecast": cash_flow,
        "summary": {
            "total_revenue": round(sum(t["amount"] for t in transactions if "Revenue" in t["category"]), 2),
            "total_expense": round(sum(t["amount"] for t in transactions if "Expense" in t["category"]), 2),
            "ar_total": round(sum(ar["amount"] for ar in ar_records), 2),
            "ar_overdue": round(sum(ar["amount"] for ar in ar_records if ar["days_overdue"] > 0), 2),
            "projected_balance": cash_flow[-1]["balance"] if cash_flow else 0
        }
    }


def _generate_expense_audit_data(case: Case) -> dict:
    company_name = case.title.split(" for ")[-1] if " for " in case.title else "Test Company"

    categories = ["Marketing", "Ops", "G&A", "Tech", "Payroll", "Logistics", "Travel"]
    departments = ["Sales", "Marketing", "Ops", "Finance", "Engineering"]
    records = []
    for _ in range(random.randint(25, 45)):
        cat = random.choice(categories)
        dept = random.choice(departments)
        amount = round(random.uniform(150, 8500), 2)
        budget = amount * random.uniform(0.85, 1.15)
        records.append({
            "date": (datetime.now() - timedelta(days=random.randint(5, 90))).strftime("%Y-%m-%d"),
            "vendor": random.choice(["AWS", "Google", "Meta", "Stripe", "Notion", "Zoom", "Figma", "Contractor LLC", "ShipCo"]),
            "amount": amount,
            "category": cat,
            "department": dept,
            "budget": round(budget, 2),
            "variance": round(amount - budget, 2),
        })

    variance_summary = {}
    for r in records:
        variance_summary.setdefault(r["department"], 0)
        variance_summary[r["department"]] += r["variance"]

    return {
        "company": company_name,
        "report_date": datetime.now().strftime("%Y-%m-%d"),
        "expenses": records,
        "variance_summary": [{"department": k, "variance": round(v, 2)} for k, v in variance_summary.items()],
        "summary": {
            "total_expense": round(sum(r["amount"] for r in records), 2),
            "over_budget_items": len([r for r in records if r["variance"] > 0]),
            "under_budget_items": len([r for r in records if r["variance"] <= 0]),
        },
    }


def _generate_revenue_forecast_data(case: Case) -> dict:
    company_name = case.title.split(" for ")[-1] if " for " in case.title else "Test Company"

    months = ["M1", "M2", "M3"]
    mrr_forecast = []
    current_mrr = random.randint(40000, 90000)
    for m in months:
        new = round(random.uniform(8000, 18000), 2)
        churn = round(random.uniform(4000, 10000), 2)
        expansion = round(random.uniform(2000, 8000), 2)
        current_mrr = current_mrr + new - churn + expansion
        mrr_forecast.append({
            "month": m,
            "new_mrr": new,
            "churn_mrr": churn,
            "expansion_mrr": expansion,
            "total_mrr": round(current_mrr, 2),
        })

    scenarios = []
    for scenario in ["Best", "Likely", "Worst"]:
        growth = random.uniform(0.08, 0.2) if scenario == "Best" else (random.uniform(0.02, 0.1) if scenario == "Likely" else random.uniform(-0.08, 0.02))
        churn_delta = random.uniform(-0.02, 0.02)
        scenarios.append({
            "scenario": scenario,
            "growth_rate": round(growth, 3),
            "churn_change": round(churn_delta, 3),
            "projected_mrr": round(current_mrr * (1 + growth + churn_delta), 2)
        })

    return {
        "company": company_name,
        "report_date": datetime.now().strftime("%Y-%m-%d"),
        "mrr_forecast": mrr_forecast,
        "scenarios": scenarios,
        "summary": {
            "ending_mrr": mrr_forecast[-1]["total_mrr"],
            "avg_new_mrr": round(sum(r["new_mrr"] for r in mrr_forecast) / len(mrr_forecast), 2),
            "avg_churn_mrr": round(sum(r["churn_mrr"] for r in mrr_forecast) / len(mrr_forecast), 2),
        },
    }


def _generate_payroll_data(case: Case) -> dict:
    company_name = case.title.split(" for ")[-1] if " for " in case.title else "Test Company"

    payroll_runs = []
    for _ in range(random.randint(12, 20)):
        gross = round(random.uniform(1500, 8500), 2)
        taxes = round(gross * random.uniform(0.18, 0.28), 2)
        benefits = round(gross * random.uniform(0.05, 0.12), 2)
        net = round(gross - taxes - benefits, 2)
        payroll_runs.append({
            "employee": random.choice(["FT", "Contractor", "Manager", "Analyst", "Engineer"]) + f" {random.randint(101, 299)}",
            "gross": gross,
            "taxes": taxes,
            "benefits": benefits,
            "net": net,
            "pay_date": (datetime.now() - timedelta(days=random.randint(3, 45))).strftime("%Y-%m-%d"),
        })

    employer_taxes = round(sum(r["gross"] for r in payroll_runs) * 0.0765, 2)

    return {
        "company": company_name,
        "report_date": datetime.now().strftime("%Y-%m-%d"),
        "payroll_runs": payroll_runs,
        "summary": {
            "total_gross": round(sum(r["gross"] for r in payroll_runs), 2),
            "total_taxes": round(sum(r["taxes"] for r in payroll_runs), 2),
            "total_benefits": round(sum(r["benefits"] for r in payroll_runs), 2),
            "total_net": round(sum(r["net"] for r in payroll_runs), 2),
            "employer_taxes": employer_taxes,
        },
    }


def _generate_analysis_mock_data(case: Case) -> dict:
    """Generate mock analysis data for testing."""
    
    # Randomize data counts
    num_metrics = random.randint(4, 8)
    num_segments = random.randint(3, 6)
    num_anomalies = random.randint(2, 6)
    
    # Sample metric data
    metrics = []
    metric_names = ["User Engagement", "Conversion Rate", "Customer Satisfaction", "Response Time", "Error Rate", "Churn Rate", "Retention Rate", "NPS Score"]
    selected_metrics = random.sample(metric_names, min(num_metrics, len(metric_names)))
    
    for metric in selected_metrics:
        current_value = round(random.uniform(60, 95), 2)
        benchmark = round(current_value - random.uniform(5, 15), 2)
        
        metrics.append({
            "metric": metric,
            "current_value": current_value,
            "benchmark_value": benchmark,
            "variance": round(current_value - benchmark, 2),
            "variance_percent": round(((current_value - benchmark) / benchmark * 100), 2),
            "trend": random.choice(["Improving", "Declining", "Stable"])
        })
    
    # Sample trend data (randomize months between 6-12)
    num_months = random.randint(6, 12)
    trends = []
    base_value = 75
    for month in range(num_months):
        trend_value = base_value + random.uniform(-10, 10)
        trends.append({
            "month": month + 1,
            "value": round(trend_value, 2),
            "change": round(trend_value - base_value, 2) if month > 0 else 0
        })
        base_value = trend_value
    
    # Sample segmentation data
    segments = []
    segment_names = ["Enterprise", "Mid-Market", "SMB", "Startup", "Trial", "Free Tier"]
    selected_segments = random.sample(segment_names, min(num_segments, len(segment_names)))
    
    for segment in selected_segments:
        segments.append({
            "segment": segment,
            "count": random.randint(10, 500),
            "revenue": round(random.uniform(5000, 100000), 2),
            "churn_rate": round(random.uniform(2, 20), 2),
            "satisfaction_score": round(random.uniform(3, 5), 2)
        })
    
    # Sample anomalies
    anomalies = []
    anomaly_types = ["Spike in error rate", "Unusual user behavior", "Data quality issue", "Performance degradation", "Traffic anomaly", "Revenue dip"]
    selected_anomalies = random.sample(anomaly_types, min(num_anomalies, len(anomaly_types)))
    
    for anomaly_type in selected_anomalies:
        anomalies.append({
            "type": anomaly_type,
            "severity": random.choice(["Low", "Medium", "High", "Critical"]),
            "detected_date": (datetime.now() - timedelta(days=random.randint(1, 30))).strftime("%Y-%m-%d"),
            "description": "Sample anomaly detected in the dataset",
            "impact": random.choice(["10%", "25%", "40%", "60%"])
        })
    
    return {
        "analysis_date": datetime.now().strftime("%Y-%m-%d"),
        "case_id": case.id,
        "metrics": metrics,
        "trends": trends,
        "segments": segments,
        "anomalies": anomalies,
        "summary": {
            "total_issues": len(anomalies),
            "critical_issues": len([a for a in anomalies if a["severity"] == "Critical"]),
            "affected_segments": len([s for s in segments if s["churn_rate"] > 10]),
            "estimated_impact": f"${round(sum(s['revenue'] for s in segments if s['churn_rate'] > 10) * 0.15, 2)}"
        }
    }


def _generate_customer_analytics_data(case: Case) -> dict:
    metrics = []
    metric_names = [
        "Repeat Purchase Rate",
        "AOV",
        "30d Retention",
        "Churn Rate",
        "CLV",
        "Signup to First Purchase",
    ]
    for metric in metric_names:
        current = round(random.uniform(0.5, 0.95) if "Rate" in metric or "Retention" in metric else random.uniform(50, 250), 2)
        benchmark = round(current - random.uniform(0.05, 0.15) * current, 2)
        metrics.append({
            "metric": metric,
            "current_value": current,
            "benchmark_value": benchmark,
            "variance": round(current - benchmark, 2),
            "variance_percent": round(((current - benchmark) / benchmark * 100), 2),
            "trend": random.choice(["Improving", "Declining", "Stable"])
        })

    segments = []
    for segment in ["Paid Social", "Organic", "Referral", "Email", "Direct"]:
        churn_rate = round(random.uniform(5, 25), 2)
        segments.append({
            "segment": segment,
            "count": random.randint(200, 2000),
            "revenue": round(random.uniform(10000, 80000), 2),
            "churn_rate": churn_rate,
            "satisfaction_score": round(random.uniform(3.2, 4.8), 2)
        })

    trends = []
    base = 100
    for month in range(6):
        val = base + random.uniform(-12, 15)
        trends.append({"month": month + 1, "value": round(val, 2), "change": round(val - base if month > 0 else 0, 2)})
        base = val

    anomalies = [
        {
            "type": "Spike in churn for Paid Social",
            "severity": random.choice(["High", "Critical"]),
            "detected_date": (datetime.now() - timedelta(days=random.randint(1, 10))).strftime("%Y-%m-%d"),
            "description": "Recent cohort shows accelerated churn",
            "impact": "25%"
        },
        {
            "type": "Attribution drop for Email",
            "severity": random.choice(["Medium", "High"]),
            "detected_date": (datetime.now() - timedelta(days=random.randint(5, 20))).strftime("%Y-%m-%d"),
            "description": "UTM tagging issues causing misattribution",
            "impact": "15%"
        }
    ]

    return {
        "analysis_date": datetime.now().strftime("%Y-%m-%d"),
        "case_id": case.id,
        "metrics": metrics,
        "trends": trends,
        "segments": segments,
        "anomalies": anomalies,
        "summary": {
            "total_issues": len(anomalies),
            "critical_issues": len([a for a in anomalies if a["severity"] == "Critical"]),
            "affected_segments": len([s for s in segments if s["churn_rate"] > 12]),
            "estimated_impact": f"${round(sum(s['revenue'] for s in segments if s['churn_rate'] > 12) * 0.2, 2)}"
        }
    }


def _generate_feature_adoption_gaps_data(case: Case) -> dict:
    """Generate mock data focused on feature adoption gaps and usage patterns."""

    features = [
        "Automation Builder",
        "Campaign Reporting",
        "Audience Segmentation",
        "A/B Testing",
        "Email Templates",
        "Integrations Hub",
    ]

    feature_usage = []
    for feature in features:
        mau = random.randint(500, 3200)
        wau = random.randint(int(mau * 0.35), int(mau * 0.85))
        dau = random.randint(int(wau * 0.35), int(wau * 0.8))
        activation = round(random.uniform(0.35, 0.78), 2)
        adoption_gap = round(random.uniform(0.05, 0.25), 2)  # share of users who stall post-activation
        stickiness = round(dau / wau, 2) if wau else 0
        feature_usage.append({
            "feature": feature,
            "dau": dau,
            "wau": wau,
            "mau": mau,
            "activation_rate": activation,
            "adoption_gap": adoption_gap,
            "stickiness": stickiness,
            "trend": random.choice(["Declining", "Flat", "Recovering", "Improving"]),
        })

    funnels = []
    funnel_steps = ["Signup", "Onboarding Complete", "First Automation", "First Report Download", "Repeat Usage"]
    base = 1.0
    for step in funnel_steps:
        drop = random.uniform(0.05, 0.22) if step != "Signup" else 0
        base = base * (1 - drop)
        funnels.append({
            "step": step,
            "conversion": round(base, 2),
            "drop_off": round(drop, 2) if step != "Signup" else 0,
        })

    cohorts = []
    for month in range(1, 7):
        start = random.uniform(0.42, 0.76)
        cohorts.append({
            "cohort_month": f"M-{month}",
            "activation_rate": round(start, 2),
            "day_30_retention": round(start * random.uniform(0.55, 0.85), 2),
            "feature_depth": round(random.uniform(1.3, 2.4), 2),  # avg distinct features used
        })

    segments = []
    for segment in ["Paid Social", "Agency Partners", "Email Subscribers", "Referral", "Direct"]:
        activation = round(random.uniform(0.38, 0.82), 2)
        depth = round(random.uniform(1.2, 2.7), 2)
        segments.append({
            "segment": segment,
            "activation_rate": activation,
            "feature_depth": depth,
            "churn_risk": round(random.uniform(0.08, 0.25), 2),
        })

    anomalies = [
        {
            "type": "Usage drop post-onboarding",
            "severity": random.choice(["High", "Critical"]),
            "detected_date": (datetime.now() - timedelta(days=random.randint(2, 10))).strftime("%Y-%m-%d"),
            "description": "Users complete onboarding but do not build first automation",
            "impact": "Feature depth down 18%",
        },
        {
            "type": "Integration errors",
            "severity": random.choice(["Medium", "High"]),
            "detected_date": (datetime.now() - timedelta(days=random.randint(8, 25))).strftime("%Y-%m-%d"),
            "description": "Third-party auth failures blocking campaign publishing",
            "impact": "15% of campaigns stuck in draft",
        },
    ]

    summary = {
        "top_gaps": sorted(feature_usage, key=lambda x: x["adoption_gap"], reverse=True)[:3],
        "suspected_root_causes": [
            "Onboarding completes without nudging first automation build",
            "Reporting value not shown in first session",
            "Integration failures causing drafts to stall",
        ],
        "recommended_actions": [
            "Trigger in-product checklist to first automation with sample templates",
            "Show time-to-value banner after report download with next best action",
            "Add retry/alert workflow for failed integrations to unblock publishing",
        ],
    }

    return {
        "analysis_date": datetime.now().strftime("%Y-%m-%d"),
        "case_id": case.id,
        "features": feature_usage,
        "funnels": funnels,
        "cohorts": cohorts,
        "segments": segments,
        "anomalies": anomalies,
        "summary": summary,
    }


def _generate_fraud_detection_data(case: Case) -> dict:
    """Generate mock data for fraud pattern detection across channels."""

    channels = ["Web", "Mobile", "Affiliate", "Gift Cards", "Campus Kiosk"]
    payment_methods = ["Credit Card", "Debit Card", "PayPal", "UPI", "Wallet"]

    transactions = []
    for _ in range(random.randint(80, 140)):
        amt = round(random.uniform(20, 650), 2)
        channel = random.choice(channels)
        method = random.choice(payment_methods)
        velocity = random.randint(1, 9)
        chargeback = random.random() < 0.08
        anomaly = random.random() < 0.12
        risk_score = round(min(99, random.uniform(15, 95) + (velocity * 2) + (25 if anomaly else 0)), 1)
        transactions.append({
            "transaction_id": f"TX-{random.randint(200000, 999999)}",
            "channel": channel,
            "payment_method": method,
            "amount": amt,
            "risk_score": risk_score,
            "is_chargeback": chargeback,
            "is_anomaly": anomaly,
            "velocity_last_24h": velocity,
            "device_reused": random.choice([True, False]),
            "geo_mismatch": random.choice([True, False]),
        })

    # Aggregate by channel and method
    channel_rollup = []
    for channel in channels:
        channel_tx = [t for t in transactions if t["channel"] == channel]
        total = len(channel_tx)
        chargebacks = len([t for t in channel_tx if t["is_chargeback"]])
        anomalies = len([t for t in channel_tx if t["is_anomaly"]])
        channel_rollup.append({
            "channel": channel,
            "volume": total,
            "fraud_rate": round(chargebacks / total, 3) if total else 0,
            "anomaly_rate": round(anomalies / total, 3) if total else 0,
            "avg_risk_score": round(sum(t["risk_score"] for t in channel_tx) / total, 1) if total else 0,
        })

    method_rollup = []
    for method in payment_methods:
        method_tx = [t for t in transactions if t["payment_method"] == method]
        total = len(method_tx)
        chargebacks = len([t for t in method_tx if t["is_chargeback"]])
        method_rollup.append({
            "payment_method": method,
            "volume": total,
            "fraud_rate": round(chargebacks / total, 3) if total else 0,
        })

    patterns = [
        {
            "pattern": "High-velocity small-dollar purchases",
            "evidence": f"{len([t for t in transactions if t['velocity_last_24h'] >= 5])} tx with 5+ repeats/24h",
            "risk": "Account takeover or testing stolen cards",
        },
        {
            "pattern": "Geo-IP mismatch",
            "evidence": f"{len([t for t in transactions if t['geo_mismatch']])} tx with geo mismatch",
            "risk": "Proxy/VPN masking location",
        },
        {
            "pattern": "Device reuse across accounts",
            "evidence": f"{len([t for t in transactions if t['device_reused']])} tx on shared devices",
            "risk": "Multi-account abuse or collusion",
        },
    ]

    anomalies = [
        {
            "type": "Chargeback spike on Affiliate",
            "severity": random.choice(["High", "Critical"]),
            "detected_date": (datetime.now() - timedelta(days=random.randint(1, 5))).strftime("%Y-%m-%d"),
            "description": "Affiliate channel shows 3x chargebacks vs baseline",
            "impact": "Refund losses rising; suspend risky affiliates",
        },
        {
            "type": "Device clustering",
            "severity": random.choice(["Medium", "High"]),
            "detected_date": (datetime.now() - timedelta(days=random.randint(6, 15))).strftime("%Y-%m-%d"),
            "description": "Shared device fingerprints across 12 accounts",
            "impact": "Likely synthetic identity ring",
        },
    ]

    summary = {
        "worst_channels": sorted(channel_rollup, key=lambda x: x["fraud_rate"], reverse=True)[:2],
        "worst_methods": sorted(method_rollup, key=lambda x: x["fraud_rate"], reverse=True)[:2],
        "recommended_actions": [
            "Tighten velocity rules on small-dollar purchases and require step-up auth",
            "Block high-risk geo-IP pairs and enforce device binding",
            "Score affiliate traffic separately; pause cohorts with elevated chargebacks",
        ],
        "root_causes": [
            "High-velocity testing of stolen cards",
            "VPN/proxy usage obscuring origin",
            "Shared devices enabling multi-account abuse",
        ],
    }

    return {
        "analysis_date": datetime.now().strftime("%Y-%m-%d"),
        "case_id": case.id,
        "transactions": transactions,
        "channel_rollup": channel_rollup,
        "payment_method_rollup": method_rollup,
        "patterns": patterns,
        "anomalies": anomalies,
        "summary": summary,
    }


def _generate_performance_metrics_data(case: Case) -> dict:
    """
    Generate SaaS product performance metrics focused on user engagement and feature adoption.
    Aligns with context: "Product experiencing performance dips. Root cause analysis of user engagement drop."
    """
    # Product engagement metrics
    metrics = []
    metric_specs = [
        ("Daily Active Users (DAU)", 1000, 3000, 200, 400),
        ("Session Length (mins)", 12, 45, 3, 8),
        ("Feature Adoption Rate (%)", 25, 78, 8, 15),
        ("Churn Rate (%)", 1.2, 4.5, 0.5, 1.2),
    ]
    
    for metric_name, curr_low, curr_high, var_low, var_high in metric_specs:
        current = round(random.uniform(curr_low, curr_high), 2)
        benchmark = round(current - random.uniform(var_low, var_high), 2)
        metrics.append({
            "metric": metric_name,
            "current_value": current,
            "benchmark_value": max(1, benchmark),
            "variance": round(current - benchmark, 2),
            "variance_percent": round(((current - benchmark) / max(benchmark, 1) * 100), 2),
            "trend": random.choice(["Improving", "Declining", "Stable"])
        })

    # Time series trend data
    trends = []
    base_dau = 2200
    base_session = 28
    for day in range(30):
        dau = base_dau + random.uniform(-300, 150)
        session_length = base_session + random.uniform(-4, 3)
        trends.append({
            "day": day + 1,
            "dau": round(dau, 0),
            "session_length": round(session_length, 2),
            "churn": round(random.uniform(1.5, 4.2), 2)
        })
        base_dau = dau
        base_session = session_length

    # Feature-level performance
    features = []
    feature_names = ["Dashboard", "Reports", "Integrations", "Collaboration", "Analytics", "Settings"]
    for feature in feature_names:
        adoption = round(random.uniform(20, 85), 1)
        features.append({
            "feature": feature,
            "adoption_rate": adoption,
            "avg_sessions_per_user": round(random.uniform(2, 25), 1),
            "session_length": round(random.uniform(3, 40), 1),
            "drop_off_rate": round(random.uniform(5, 35), 1),
            "user_satisfaction": round(random.uniform(3.0, 4.8), 2)
        })

    # Cohort analysis
    cohorts = []
    cohort_names = ["Week 1", "Week 2-4", "Month 2", "Month 3+"]
    for cohort in cohort_names:
        cohorts.append({
            "cohort": cohort,
            "retention_day_7": round(random.uniform(35, 85), 1),
            "retention_day_30": round(random.uniform(15, 60), 1),
            "lifetime_sessions": round(random.uniform(10, 200), 0),
            "churn_rate": round(random.uniform(1, 8), 1)
        })

    # Anomalies tied to engagement drop
    anomalies = [
        {
            "type": "Dashboard adoption drop",
            "severity": "Critical",
            "detected_date": (datetime.now() - timedelta(days=3)).strftime("%Y-%m-%d"),
            "description": "Dashboard feature adoption decreased from 78% to 52% following UI redesign",
            "impact": "Affecting 1,100+ users, 35% drop in daily usage",
            "affected_feature": "Dashboard"
        },
        {
            "type": "New user onboarding friction",
            "severity": "High",
            "detected_date": (datetime.now() - timedelta(days=8)).strftime("%Y-%m-%d"),
            "description": "Week 1 cohort retention dropped 22% this month vs. prior months",
            "impact": "200 new users lost in 7 days, affecting signup-to-activation",
            "affected_feature": "Onboarding"
        },
        {
            "type": "Session length degradation",
            "severity": "High",
            "detected_date": (datetime.now() - timedelta(days=12)).strftime("%Y-%m-%d"),
            "description": "Average session length declined from 32 mins to 18 mins over 14 days",
            "impact": "Users spending less time per session, suggests reduced engagement",
            "affected_feature": "Core Product"
        }
    ]

    return {
        "analysis_date": datetime.now().strftime("%Y-%m-%d"),
        "case_id": case.id,
        "product": "SaaS Platform",
        "metrics": metrics,
        "trends": trends,
        "features": features,
        "cohorts": cohorts,
        "anomalies": anomalies,
        "summary": {
            "total_issues": len(anomalies),
            "critical_issues": len([a for a in anomalies if a["severity"] == "Critical"]),
            "affected_features": len([f for f in features if f["drop_off_rate"] > 20]),
            "at_risk_cohorts": len([c for c in cohorts if c["churn_rate"] > 4]),
            "total_users_impacted": 1300,
            "engagement_drop_percent": 22.5
        }
    }


def _generate_api_performance_nonprofit_data(case: Case) -> dict:
    """
    Generate API performance data for nonprofit organization scenario.
    Metrics focus on request/response time analysis and system reliability.
    """
    # API-specific metrics aligned with the nonprofit investigation context
    metrics = []
    metric_specs = [
        ("Response Time (ms)", 150, 400, 40, 80),  # (name, base_current_low, base_current_high, variance_low, variance_high)
        ("Error Rate (%)", 0.5, 3.2, 0.3, 1.5),
        ("Request Throughput (req/s)", 100, 500, 20, 100),
        ("Database Query Time (ms)", 50, 200, 10, 40),
    ]
    
    for metric_name, curr_low, curr_high, var_low, var_high in metric_specs:
        current = round(random.uniform(curr_low, curr_high), 2)
        benchmark = round(current - random.uniform(var_low, var_high), 2)
        metrics.append({
            "metric": metric_name,
            "current_value": current,
            "benchmark_value": max(0.1, benchmark),  # Ensure benchmark doesn't go negative
            "variance": round(current - benchmark, 2),
            "variance_percent": round(((current - benchmark) / max(benchmark, 0.1) * 100), 2),
            "trend": random.choice(["Improving", "Declining", "Stable"])
        })

    # Time series data for trend analysis over past 30 days
    trends = []
    base_response_time = 280
    base_error_rate = 2.1
    for day in range(30):
        response_time = base_response_time + random.uniform(-50, 80)
        error_rate = base_error_rate + random.uniform(-0.8, 1.5)
        trends.append({
            "day": day + 1,
            "response_time": round(response_time, 2),
            "error_rate": round(max(0.1, error_rate), 2),
            "request_count": random.randint(1000, 5000)
        })
        base_response_time = response_time
        base_error_rate = error_rate

    # Endpoint-level breakdown (key API endpoints)
    endpoints = []
    endpoint_names = [
        "/api/v1/applications",
        "/api/v1/beneficiary-lookup",
        "/api/v1/eligibility-check",
        "/api/v1/document-upload",
        "/api/v1/reporting/monthly",
    ]
    
    for endpoint in endpoint_names:
        endpoints.append({
            "endpoint": endpoint,
            "avg_response_time": round(random.uniform(80, 350), 2),
            "p95_latency": round(random.uniform(200, 600), 2),
            "p99_latency": round(random.uniform(300, 900), 2),
            "error_rate": round(random.uniform(0.1, 4.5), 2),
            "request_count": random.randint(500, 3000),
            "affected_users": random.randint(50, 500)
        })

    # Business impact by affected area
    affected_areas = []
    area_names = [
        {"name": "Beneficiary Enrollment", "impact": "High", "users_affected": random.randint(100, 300)},
        {"name": "Application Processing", "impact": "Critical", "users_affected": random.randint(200, 500)},
        {"name": "Reporting & Analytics", "impact": "Medium", "users_affected": random.randint(50, 150)},
        {"name": "Document Management", "impact": "High", "users_affected": random.randint(80, 200)},
    ]
    affected_areas = [a for a in area_names]

    # Root cause anomalies
    anomalies = [
        {
            "type": "Database connection pool exhaustion",
            "severity": "Critical",
            "detected_date": (datetime.now() - timedelta(days=2)).strftime("%Y-%m-%d"),
            "description": "Connection pool at 95% capacity causing request queueing and timeout errors",
            "impact": "Affected 250+ concurrent users on Application Processing endpoint",
            "affected_endpoint": "/api/v1/applications"
        },
        {
            "type": "Slow N+1 query on beneficiary lookup",
            "severity": "High",
            "detected_date": (datetime.now() - timedelta(days=5)).strftime("%Y-%m-%d"),
            "description": "Unoptimized query loading related records sequentially instead of in batch",
            "impact": "Response time increased from 120ms to 450ms for this endpoint",
            "affected_endpoint": "/api/v1/beneficiary-lookup"
        },
        {
            "type": "Memory leak in document upload service",
            "severity": "High",
            "detected_date": (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d"),
            "description": "Temporary files not being cleaned up after upload processing",
            "impact": "Gradual service degradation and increased error rate on file operations",
            "affected_endpoint": "/api/v1/document-upload"
        }
    ]

    return {
        "analysis_date": datetime.now().strftime("%Y-%m-%d"),
        "case_id": case.id,
        "organization_type": "Nonprofit - Digital Services",
        "metrics": metrics,
        "time_series": trends,
        "endpoints": endpoints,
        "affected_business_areas": affected_areas,
        "anomalies": anomalies,
        "summary": {
            "total_root_causes": len(anomalies),
            "critical_issues": len([a for a in anomalies if a["severity"] == "Critical"]),
            "affected_endpoints": len([e for e in endpoints if e["error_rate"] > 1.5]),
            "avg_response_time_increase": f"{round(random.uniform(35, 95), 1)}%",
            "users_impacted": sum(a["users_affected"] for a in affected_areas),
            "business_impact": "Service reliability degradation affecting mission-critical workflows"
        }
    }


def _generate_marketing_funnel_data(case: Case) -> dict:
    metrics = []
    for metric in ["CTR", "Signup CVR", "MQL->SQL", "CAC", "LTV/CAC", "30d Retention"]:
        current = round(random.uniform(0.8, 5.0), 2) if metric in ["CTR", "Signup CVR", "MQL->SQL"] else round(random.uniform(80, 450), 2)
        benchmark = round(current - random.uniform(-0.5, 1.5), 2) if metric in ["CTR", "Signup CVR", "MQL->SQL"] else round(current - random.uniform(-40, 60), 2)
        metrics.append({
            "metric": metric,
            "current_value": current,
            "benchmark_value": benchmark,
            "variance": round(current - benchmark, 2),
            "variance_percent": round(((current - benchmark) / benchmark * 100) if benchmark else 0, 2),
            "trend": random.choice(["Improving", "Declining", "Stable"])
        })

    trends = []
    base = 3.0
    for month in range(6):
        val = base + random.uniform(-0.8, 1.2)
        trends.append({"month": month + 1, "value": round(val, 2), "change": round(val - base if month > 0 else 0, 2)})
        base = val

    segments = []
    for channel in ["Paid", "Organic", "Referral", "Email", "Affiliate"]:
        segments.append({
            "segment": channel,
            "count": random.randint(300, 4000),
            "revenue": round(random.uniform(8000, 60000), 2),
            "churn_rate": round(random.uniform(4, 22), 2),
            "satisfaction_score": round(random.uniform(3.0, 4.6), 2)
        })

    anomalies = [
        {
            "type": "Attribution mismatch in Paid",
            "severity": random.choice(["Medium", "High"]),
            "detected_date": (datetime.now() - timedelta(days=3)).strftime("%Y-%m-%d"),
            "description": "Spend recorded without conversions",
            "impact": "20%"
        },
        {
            "type": "Referral spike",
            "severity": random.choice(["Low", "Medium"]),
            "detected_date": (datetime.now() - timedelta(days=8)).strftime("%Y-%m-%d"),
            "description": "Untracked campaign driving traffic",
            "impact": "12%"
        }
    ]

    return {
        "analysis_date": datetime.now().strftime("%Y-%m-%d"),
        "case_id": case.id,
        "metrics": metrics,
        "trends": trends,
        "segments": segments,
        "anomalies": anomalies,
        "summary": {
            "total_issues": len(anomalies),
            "critical_issues": len([a for a in anomalies if a["severity"] == "Critical"]),
            "affected_segments": len([s for s in segments if s["churn_rate"] > 12]),
            "estimated_impact": f"${round(sum(s['revenue'] for s in segments if s['churn_rate'] > 12) * 0.18, 2)}"
        }
    }


def _generate_ops_sla_data(case: Case) -> dict:
    metrics = []
    for metric in ["SLA Attainment %", "Backlog Aging (hrs)", "First Contact Resolution %", "Avg Handle Time (mins)"]:
        current = round(random.uniform(65, 95), 2) if "%" in metric else round(random.uniform(4, 36), 2)
        benchmark = round(current - random.uniform(-8, 12), 2) if "%" in metric else round(current - random.uniform(-4, 6), 2)
        metrics.append({
            "metric": metric,
            "current_value": current,
            "benchmark_value": benchmark,
            "variance": round(current - benchmark, 2),
            "variance_percent": round(((current - benchmark) / benchmark * 100) if benchmark else 0, 2),
            "trend": random.choice(["Improving", "Declining", "Stable"])
        })

    trends = []
    base = 80
    for month in range(6):
        val = base + random.uniform(-10, 10)
        trends.append({"month": month + 1, "value": round(val, 2), "change": round(val - base if month > 0 else 0, 2)})
        base = val

    segments = []
    for segment in ["NA", "EMEA", "APAC"]:
        churn = round(random.uniform(4, 18), 2)
        segments.append({
            "segment": segment,
            "count": random.randint(400, 2500),
            "revenue": round(random.uniform(12000, 70000), 2),
            "churn_rate": churn,
            "satisfaction_score": round(random.uniform(3.1, 4.5), 2)
        })

    anomalies = [
        {
            "type": "Backlog surge in EMEA",
            "severity": random.choice(["High", "Critical"]),
            "detected_date": (datetime.now() - timedelta(days=4)).strftime("%Y-%m-%d"),
            "description": "Staffing gap during peak period",
            "impact": "22%"
        },
        {
            "type": "Quality dip in NA",
            "severity": random.choice(["Medium", "High"]),
            "detected_date": (datetime.now() - timedelta(days=9)).strftime("%Y-%m-%d"),
            "description": "Training backlog causing reopens",
            "impact": "15%"
        }
    ]

    return {
        "analysis_date": datetime.now().strftime("%Y-%m-%d"),
        "case_id": case.id,
        "metrics": metrics,
        "trends": trends,
        "segments": segments,
        "anomalies": anomalies,
        "summary": {
            "total_issues": len(anomalies),
            "critical_issues": len([a for a in anomalies if a["severity"] == "Critical"]),
            "affected_segments": len([s for s in segments if s["churn_rate"] > 10]),
            "estimated_impact": f"${round(sum(s['revenue'] for s in segments if s['churn_rate'] > 10) * 0.14, 2)}"
        }
    }


def format_mock_data_summary(mock_data: dict) -> str:
    """Format mock data into a readable summary string that tolerates varied shapes."""
    summary = mock_data.get("summary", {}) or {}

    def as_money(value) -> str:
        try:
            return f"${float(value):,.2f}"
        except Exception:
            return str(value)

    # Data quality/inconsistency analysis
    if "metrics_by_department" in mock_data:
        return f"""Mock Data Quality Analysis Generated for: {mock_data.get('company', 'n/a')}
Analysis Date: {mock_data.get('analysis_date', 'n/a')}

Summary:
- Total Metrics Analyzed: {summary.get('total_metrics_analyzed', 'n/a')}
- Metrics with Significant Variance: {summary.get('metrics_with_significant_variance', 'n/a')}
- Departments Affected: {summary.get('departments_affected', 'n/a')}
- Critical Issues: {summary.get('critical_issues', 'n/a')}
- Highest Variance: {summary.get('highest_variance_metric', 'n/a')} ({summary.get('max_variance_percent', 'n/a')}%)
- Key Finding: {summary.get('key_finding', 'n/a')}

Data Points Generated:
- {len(mock_data.get('metrics_by_department', []))} metrics with department breakdowns
- {len(mock_data.get('data_sources', []))} data sources analyzed
- {len(mock_data.get('discrepancy_causes', []))} root causes identified
- {len(mock_data.get('anomalies', []))} anomalies detected"""

    # Data quality/inconsistency analysis
    if "metrics_by_department" in mock_data:
        return f"""Mock Data Quality Analysis Generated for: {mock_data.get('company', 'n/a')}
Analysis Date: {mock_data.get('analysis_date', 'n/a')}

Summary:
- Total Metrics Analyzed: {summary.get('total_metrics_analyzed', 'n/a')}
- Metrics with Significant Variance: {summary.get('metrics_with_significant_variance', 'n/a')}
- Departments Affected: {summary.get('departments_affected', 'n/a')}
- Critical Issues: {summary.get('critical_issues', 'n/a')}
- Highest Variance: {summary.get('highest_variance_metric', 'n/a')} ({summary.get('max_variance_percent', 'n/a')}%)
- Key Finding: {summary.get('key_finding', 'n/a')}

Data Points Generated:
- {len(mock_data.get('metrics_by_department', []))} metrics with department breakdowns
- {len(mock_data.get('data_sources', []))} data sources analyzed
- {len(mock_data.get('discrepancy_causes', []))} root causes identified
- {len(mock_data.get('anomalies', []))} anomalies detected"""

    # Social media sentiment analysis
    if "platform_sentiment" in mock_data:
        return f"""Mock Social Media Sentiment Analysis Generated for: {mock_data.get('company', 'n/a')}
Analysis Date: {mock_data.get('analysis_date', 'n/a')}

Summary:
- Overall Sentiment Score: {summary.get('overall_sentiment_score', 'n/a')}
- Platforms Analyzed: {summary.get('platforms_analyzed', 'n/a')}
- Total Mentions: {summary.get('total_mentions_analyzed', 'n/a'):,}
- Overall Positive: {summary.get('overall_positive_percent', 'n/a')}%
- Overall Negative: {summary.get('overall_negative_percent', 'n/a')}%
- Share of Voice: {summary.get('share_of_voice', 'n/a')}%
- Best Platform: {summary.get('best_platform', 'n/a')}
- Critical Issues: {summary.get('critical_issues', 'n/a')}
- Key Finding: {summary.get('key_finding', 'n/a')}

Data Points Generated:
- {len(mock_data.get('platform_sentiment', []))} platforms analyzed
- {len(mock_data.get('mention_trends', []))} days of trend data
- {len(mock_data.get('hashtags', []))} top campaigns tracked
- {len(mock_data.get('sentiment_drivers', []))} sentiment drivers identified
- {len(mock_data.get('anomalies', []))} anomalies detected"""

    # Social media sentiment analysis
    if "platform_sentiment" in mock_data:
        return f"""Mock Social Media Sentiment Analysis Generated for: {mock_data.get('company', 'n/a')}
Analysis Date: {mock_data.get('analysis_date', 'n/a')}

Summary:
- Overall Sentiment Score: {summary.get('overall_sentiment_score', 'n/a')}
- Platforms Analyzed: {summary.get('platforms_analyzed', 'n/a')}
- Total Mentions: {summary.get('total_mentions_analyzed', 'n/a'):,}
- Overall Positive: {summary.get('overall_positive_percent', 'n/a')}%
- Overall Negative: {summary.get('overall_negative_percent', 'n/a')}%
- Share of Voice: {summary.get('share_of_voice', 'n/a')}%
- Best Platform: {summary.get('best_platform', 'n/a')}
- Critical Issues: {summary.get('critical_issues', 'n/a')}
- Key Finding: {summary.get('key_finding', 'n/a')}

Data Points Generated:
- {len(mock_data.get('platform_sentiment', []))} platforms analyzed
- {len(mock_data.get('mention_trends', []))} days of trend data
- {len(mock_data.get('hashtags', []))} top campaigns tracked
- {len(mock_data.get('sentiment_drivers', []))} sentiment drivers identified
- {len(mock_data.get('anomalies', []))} anomalies detected"""

    # Marketing attribution quality analysis
    if "channel_attribution_models" in mock_data and "utm_tracking_issues" in mock_data:
        return f"""Mock Marketing Attribution Quality Analysis Generated for: {mock_data.get('company', 'n/a')}
Analysis Date: {mock_data.get('analysis_date', 'n/a')}

Summary:
- Channels Analyzed: {summary.get('channels_analyzed', 'n/a')}
- Attribution Models Analyzed: {summary.get('attribution_models_analyzed', 'n/a')}
- Avg Channel Credit Variance: {summary.get('avg_channel_credit_variance', 'n/a')}%
- Channels with Low Agreement: {summary.get('channels_with_low_agreement', 'n/a')}
- Data Sources Reconciled: {summary.get('data_sources_reconciled', 'n/a')}
- Max Conversion Discrepancy: {summary.get('max_conversion_discrepancy', 'n/a')} ({summary.get('max_discrepancy_percent', 'n/a')}%)
- UTM Issues Identified: {summary.get('utm_issues_identified', 'n/a')}
- Total Unattributed Traffic: {summary.get('total_unattributed_traffic', 'n/a'):,}
- Critical Issues: {summary.get('critical_issues', 'n/a')}
- Key Finding: {summary.get('key_finding', 'n/a')}

Data Points Generated:
- {len(mock_data.get('channel_attribution_models', []))} channel attribution models analyzed
- {len(mock_data.get('data_sources', []))} data sources reconciled
- {len(mock_data.get('utm_tracking_issues', []))} UTM tracking issues identified
- {len(mock_data.get('anomalies', []))} data pipeline anomalies detected"""

    # Mobile app user behavior analysis
    if "feature_metrics" in mock_data and "user_funnel" in mock_data:
        return f"""Mock Mobile App User Behavior Analysis Generated for: {mock_data.get('company', 'n/a')}
Analysis Date: {mock_data.get('analysis_date', 'n/a')}

Summary:
- Total App Users: {summary.get('total_app_users', 'n/a'):,}
- Total Features: {summary.get('total_features', 'n/a')}
- Well-Discovered Features: {summary.get('well_discovered_features', 'n/a')}
- Poorly-Discovered Features: {summary.get('poorly_discovered_features', 'n/a')}
- Critical Discoverability Issues: {summary.get('critical_discoverability_issues', 'n/a')}
- Overall 30d Retention: {summary.get('overall_retention_d30', 'n/a')}
- Overall Churn Rate: {summary.get('overall_churn_rate', 'n/a')}
- Largest At-Risk Segment: {summary.get('largest_at_risk_segment', 'n/a')}
- Key Finding: {summary.get('key_finding', 'n/a')}

Data Points Generated:
- {len(mock_data.get('feature_metrics', []))} features analyzed
- {len(mock_data.get('user_funnel', []))} funnel stages tracked
- {len(mock_data.get('cohorts', []))} cohorts analyzed
- {len(mock_data.get('user_segments', []))} user segments profiled
- {len(mock_data.get('discoverability_issues', []))} discoverability issues identified
- {len(mock_data.get('churn_analysis', []))} churn drivers analyzed
- {len(mock_data.get('anomalies', []))} critical anomalies detected"""

    # Recruitment data
    if "funnel" in mock_data and "sources" in mock_data:
        return f"""Mock Recruitment Analysis Generated for: {mock_data.get('company', 'n/a')}
Analysis Date: {mock_data.get('analysis_date', 'n/a')}

Summary:
- Total Applications: {summary.get('total_applications_received', 'n/a')}
- Offers Extended: {summary.get('total_offers_extended', 'n/a')}
- Offers Accepted: {summary.get('total_offers_accepted', 'n/a')}
- Overall Conversion Rate: {summary.get('overall_conversion_rate', 'n/a')}%
- Avg Days to Hire: {summary.get('avg_days_to_hire', 'n/a')}
- Critical Bottlenecks: {summary.get('critical_bottlenecks', 'n/a')}
- Open Positions: {summary.get('open_positions', 'n/a')}
- Key Issue: {summary.get('key_issue', 'n/a')}

Data Points Generated:
- {len(mock_data.get('funnel', []))} funnel stages
- {len(mock_data.get('sources', []))} source channels
- {len(mock_data.get('time_to_hire_by_role', []))} roles analyzed
- {len(mock_data.get('time_series', []))} days of time-series data
- {len(mock_data.get('bottlenecks', []))} bottlenecks identified
- {len(mock_data.get('anomalies', []))} anomalies detected"""

    # Fraud-focused data
    if "channel_rollup" in mock_data and "payment_method_rollup" in mock_data:
        worst_channels = ", ".join(c.get("channel", "n/a") for c in summary.get("worst_channels", [])) or "n/a"
        worst_methods = ", ".join(m.get("payment_method", "n/a") for m in summary.get("worst_methods", [])) or "n/a"
        actions = len(summary.get("recommended_actions", []))
        return f"""Mock Fraud Data Generated
Analysis Date: {mock_data.get('analysis_date', 'n/a')}

Summary:
- Worst Channels: {worst_channels}
- Worst Payment Methods: {worst_methods}
- Recommended Actions: {actions}

Data Points Generated:
- {len(mock_data.get('transactions', []))} transactions
- {len(mock_data.get('channel_rollup', []))} channel aggregates
- {len(mock_data.get('payment_method_rollup', []))} payment method aggregates"""

    # Cash flow / AR hygiene
    if "cash_flow_weekly" in mock_data:
        return f"""Mock Cash Flow Data Generated for: {mock_data.get('company', 'n/a')}
Report Date: {mock_data.get('report_date', 'n/a')}

Summary:
- Total AR Outstanding: {as_money(summary.get('total_ar_outstanding', 0))}
- AR Overdue: {as_money(summary.get('ar_overdue', 0))}
- Current Cash Balance: {as_money(summary.get('current_cash_balance', 0))}
- Weeks of Runway: {summary.get('weeks_of_runway', 'n/a')}

Data Points Generated:
- {len(mock_data.get('retainers', []))} retainers
- {len(mock_data.get('ar_records', []))} AR records
- {len(mock_data.get('cash_flow_weekly', []))} weeks of cash flow
- {len(mock_data.get('disbursements', []))} disbursements"""

    # Expense audit
    if "expenses" in mock_data:
        return f"""Mock Expense Audit Data Generated for: {mock_data.get('company', 'n/a')}
Report Date: {mock_data.get('report_date', 'n/a')}

Summary:
- Total Expense: {as_money(summary.get('total_expense', 0))}
- Over Budget Items: {summary.get('over_budget_items', 'n/a')}
- Under Budget Items: {summary.get('under_budget_items', 'n/a')}

Data Points Generated:
- {len(mock_data.get('expenses', []))} expense records
- {len(mock_data.get('variance_summary', []))} variance summaries"""

    # Payroll
    if "payroll_runs" in mock_data:
        return f"""Mock Payroll Data Generated for: {mock_data.get('company', 'n/a')}
Report Date: {mock_data.get('report_date', 'n/a')}

Summary:
- Total Gross: {as_money(summary.get('total_gross', 0))}
- Total Taxes: {as_money(summary.get('total_taxes', 0))}
- Total Benefits: {as_money(summary.get('total_benefits', 0))}
- Total Net: {as_money(summary.get('total_net', 0))}
- Employer Taxes: {as_money(summary.get('employer_taxes', 0))}

Data Points Generated:
- {len(mock_data.get('payroll_runs', []))} payroll runs"""

    # Revenue forecast
    if "mrr_forecast" in mock_data:
        return f"""Mock Revenue Forecast Data Generated for: {mock_data.get('company', 'n/a')}
Report Date: {mock_data.get('report_date', 'n/a')}

Summary:
- Ending MRR: {as_money(summary.get('ending_mrr', 0))}
- Avg New MRR: {as_money(summary.get('avg_new_mrr', 0))}
- Avg Churn MRR: {as_money(summary.get('avg_churn_mrr', 0))}

Data Points Generated:
- {len(mock_data.get('mrr_forecast', []))} monthly forecasts
- {len(mock_data.get('scenarios', []))} scenarios"""

    # General financial (transactions/ar/cash flow forecast)
    if "transactions" in mock_data:
        return f"""Mock Financial Data Generated for: {mock_data.get('company', 'n/a')}
Report Date: {mock_data.get('report_date', 'n/a')}

Summary Metrics:
- Total Revenue: {as_money(summary.get('total_revenue', 0))}
- Total Expenses: {as_money(summary.get('total_expense', 0))}
- AR Total Outstanding: {as_money(summary.get('ar_total', 0))}
- AR Overdue: {as_money(summary.get('ar_overdue', 0))}
- Projected Balance: {as_money(summary.get('projected_balance', 0))}

Data Points Generated:
- {len(mock_data.get('transactions', []))} transactions
- {len(mock_data.get('ar_aging', []))} AR records
- {len(mock_data.get('cash_flow_forecast', []))} weeks of cash flow forecast"""

    # Analysis / performance / adoption / ops data (catch-all)
    analysis_lines = []
    if "total_issues" in summary:
        analysis_lines.append(f"Total Issues Found: {summary.get('total_issues')}")
    if "total_root_causes" in summary:
        analysis_lines.append(f"Total Root Causes: {summary.get('total_root_causes')}")
    if "critical_issues" in summary:
        analysis_lines.append(f"Critical Issues: {summary.get('critical_issues')}")
    if "affected_segments" in summary:
        analysis_lines.append(f"Affected Segments: {summary.get('affected_segments')}")
    if "affected_features" in summary:
        analysis_lines.append(f"Affected Features: {summary.get('affected_features')}")
    if "estimated_impact" in summary:
        analysis_lines.append(f"Estimated Impact: {summary.get('estimated_impact')}")
    if "users_impacted" in summary:
        analysis_lines.append(f"Users Impacted: {summary.get('users_impacted')}")
    if "business_impact" in summary:
        analysis_lines.append(f"Business Impact: {summary.get('business_impact')}")

    summary_block = "\n".join(f"- {line}" for line in analysis_lines) if analysis_lines else "- Summary data not available"
    trend_points = len(mock_data.get("trends", mock_data.get("time_series", [])))

    return f"""Mock Analysis Data Generated
Analysis Date: {mock_data.get('analysis_date', 'n/a')}

Summary:
{summary_block}

Data Points Generated:
- {len(mock_data.get('metrics', []))} key metrics
- {trend_points} trend points
- {len(mock_data.get('segments', []))} segments
- {len(mock_data.get('features', []))} features
- {len(mock_data.get('anomalies', []))} anomalies detected"""


def _generate_recruitment_analysis_data(case: Case) -> dict:
    """
    Generate hiring/recruitment analysis data for a company experiencing recruitment bottlenecks.
    Focuses on funnel conversion, time-to-hire, source performance, and drop-off analysis.
    """
    # Recruitment funnel stages
    funnel_stages = [
        "Job Posted",
        "Applications Received",
        "Phone Screen Passed",
        "Interview 1 Passed",
        "Interview 2 Passed",
        "Offer Extended",
        "Offer Accepted",
        "Onboarded"
    ]
    
    # Funnel analysis - shows drop-off at each stage
    funnel = []
    starting_applications = 500
    current_count = starting_applications
    for i, stage in enumerate(funnel_stages):
        if i == 0:
            funnel.append({
                "stage": stage,
                "count": 1,
                "conversion_rate": 100.0,
                "drop_off_rate": 0.0
            })
        else:
            drop_rate = random.uniform(0.25, 0.65)  # 25-65% drop-off at each stage
            current_count = int(current_count * (1 - drop_rate))
            conversion = round((current_count / starting_applications) * 100, 2)
            funnel.append({
                "stage": stage,
                "count": max(0, current_count),
                "conversion_rate": conversion,
                "drop_off_rate": round(drop_rate * 100, 2)
            })
    
    # Source channel performance (where candidates come from)
    sources = []
    source_names = ["LinkedIn Ads", "Referrals", "Job Board (Indeed/ZipRecruiter)", "Recruiter Outreach", "University Campus", "Internal"]
    for source in source_names:
        total_applications = random.randint(40, 200)
        phone_screen_passed = int(total_applications * random.uniform(0.15, 0.35))
        offers_extended = int(phone_screen_passed * random.uniform(0.15, 0.30))
        offers_accepted = int(offers_extended * random.uniform(0.60, 0.85))
        
        sources.append({
            "source": source,
            "total_applications": total_applications,
            "phone_screen_passed": phone_screen_passed,
            "offers_extended": offers_extended,
            "offers_accepted": offers_accepted,
            "application_to_offer_rate": round((offers_extended / total_applications * 100), 2) if total_applications else 0,
            "offer_acceptance_rate": round((offers_accepted / offers_extended * 100), 2) if offers_extended else 0,
            "quality_score": round(random.uniform(2.5, 4.8), 2)
        })
    
    # Time-to-hire metrics by role
    roles = ["Security Engineer", "Penetration Tester", "Security Analyst", "DevSecOps Engineer", "Security Architect"]
    time_to_hire_by_role = []
    for role in roles:
        time_to_hire = random.randint(35, 120)  # days
        posted_to_first_screen = random.randint(3, 15)
        screen_to_offer = random.randint(20, 60)
        offer_to_acceptance = random.randint(5, 30)
        time_to_hire_by_role.append({
            "role": role,
            "avg_days_to_hire": time_to_hire,
            "posted_to_first_screen_days": posted_to_first_screen,
            "screen_to_offer_days": screen_to_offer,
            "offer_to_acceptance_days": offer_to_acceptance,
            "candidates_in_pipeline": random.randint(3, 15),
            "current_openings": random.randint(1, 5)
        })
    
    # Metrics by time period (30-day rolling window)
    time_series = []
    base_daily_apps = 25
    for day in range(30):
        daily_apps = base_daily_apps + random.uniform(-8, 12)
        phone_screens = int(daily_apps * random.uniform(0.2, 0.4))
        interviews = int(phone_screens * random.uniform(0.3, 0.5))
        offers = int(interviews * random.uniform(0.15, 0.3))
        time_series.append({
            "day": day + 1,
            "applications_received": int(daily_apps),
            "phone_screens_completed": phone_screens,
            "interviews_conducted": interviews,
            "offers_extended": offers,
            "avg_time_to_hire_rolling": round(random.uniform(40, 95), 1)
        })
        base_daily_apps = daily_apps
    
    # Bottleneck analysis - identifies where candidates are getting stuck
    bottlenecks = [
        {
            "stage": "Application to Phone Screen",
            "severity": random.choice(["Critical", "High"]),
            "conversion_rate": round(random.uniform(0.12, 0.28), 3),
            "candidates_stuck": random.randint(280, 420),
            "description": "High volume of applications but low phone screen conversion suggests filtering issues or large applicant pool",
            "impact": "Recruiters spending too much time reviewing unqualified candidates"
        },
        {
            "stage": "Interview Stage 2 to Offer",
            "severity": random.choice(["High", "Critical"]),
            "conversion_rate": round(random.uniform(0.12, 0.25), 3),
            "candidates_stuck": random.randint(35, 65),
            "description": "Interviews progressing but fewer offers being extended; possible assessment rigor or role misfit",
            "impact": "Qualified candidates being rejected; longer time-to-hire for individual positions"
        },
        {
            "stage": "Offer Acceptance",
            "severity": random.choice(["Medium", "High"]),
            "conversion_rate": round(random.uniform(0.68, 0.82), 3),
            "candidates_stuck": random.randint(8, 18),
            "description": "Offers extended but acceptance rate below market benchmarks (typically 75-85% for tech)",
            "impact": "Candidates declining offers; need to improve offer package or employer brand"
        }
    ]
    
    # Root cause anomalies
    anomalies = [
        {
            "type": "LinkedIn source declining",
            "severity": "High",
            "detected_date": (datetime.now() - timedelta(days=5)).strftime("%Y-%m-%d"),
            "description": "LinkedIn job ad performance dropped 45% in past 2 weeks; possibly due to increased competition or ad fatigue",
            "impact": "LinkedIn was primary pipeline; now candidates drying up from this channel",
            "affected_area": "Top-of-funnel candidate generation"
        },
        {
            "type": "Offer acceptance declining",
            "severity": "High",
            "detected_date": (datetime.now() - timedelta(days=8)).strftime("%Y-%m-%d"),
            "description": "Offer acceptance rate dropped from 82% to 68% in past 3 weeks; competitors raising salaries",
            "impact": "Need to close larger gap between offer and acceptance; losing candidates to competing offers",
            "affected_area": "Offer stage conversion"
        },
        {
            "type": "DevSecOps engineer backlog",
            "severity": "Critical",
            "detected_date": (datetime.now() - timedelta(days=2)).strftime("%Y-%m-%d"),
            "description": "2 open DevSecOps roles with 52-day average time-to-hire; high technical bar screening out candidates",
            "impact": "Critical team scaling delayed; existing engineers overloaded supporting infrastructure",
            "affected_area": "Specific role bottleneck"
        }
    ]
    
    # Metrics summary
    total_applications = sum(s["total_applications"] for s in sources)
    total_offers = sum(s["offers_extended"] for s in sources)
    total_accepted = sum(s["offers_accepted"] for s in sources)
    overall_conversion = round((total_accepted / total_applications * 100), 2) if total_applications else 0
    
    return {
        "analysis_date": datetime.now().strftime("%Y-%m-%d"),
        "case_id": case.id,
        "company": case.title.split(" for ")[-1] if " for " in case.title else "Cybersecurity Firm",
        "funnel": funnel,
        "sources": sources,
        "time_to_hire_by_role": time_to_hire_by_role,
        "time_series": time_series,
        "bottlenecks": bottlenecks,
        "anomalies": anomalies,
        "summary": {
            "total_applications_received": total_applications,
            "total_offers_extended": total_offers,
            "total_offers_accepted": total_accepted,
            "overall_conversion_rate": overall_conversion,
            "critical_bottlenecks": len([b for b in bottlenecks if b["severity"] == "Critical"]),
            "avg_days_to_hire": round(sum(r["avg_days_to_hire"] for r in time_to_hire_by_role) / len(time_to_hire_by_role), 1),
            "best_source": max(sources, key=lambda x: x["offer_acceptance_rate"])["source"],
            "worst_source": min(sources, key=lambda x: x["offer_acceptance_rate"])["source"],
            "open_positions": sum(r["current_openings"] for r in time_to_hire_by_role),
            "candidates_in_pipeline": sum(r["candidates_in_pipeline"] for r in time_to_hire_by_role),
            "key_issue": "High drop-off from application to phone screen combined with declining offer acceptance rates"
        }
    }


def _generate_data_quality_analysis_data(case: Case) -> dict:
    """
    Generate data quality and metric inconsistency analysis for departments reporting conflicting metrics.
    Focuses on identifying reconciliation gaps, system misalignments, and data accuracy issues.
    """
    departments = ["Analytics", "Product", "Marketing", "Operations", "Finance", "Engineering"]
    
    # Metric inconsistencies across departments
    metrics_by_dept = []
    metric_names = ["User Engagement", "Error Rate", "NPS Score", "Churn Rate", "Conversion Rate"]
    
    for metric_name in metric_names:
        dept_values = []
        base_value = round(random.uniform(60, 95), 2)
        variance = random.uniform(5, 25)  # Departments report different values
        
        for dept in departments:
            reported_value = round(base_value + random.uniform(-variance, variance), 2)
            dept_values.append({
                "department": dept,
                "reported_value": reported_value,
                "data_source": random.choice(["Google Analytics", "Amplitude", "Mixpanel", "Custom Dashboard", "Internal DB", "Third-party API"]),
                "last_updated": (datetime.now() - timedelta(days=random.randint(0, 7))).strftime("%Y-%m-%d %H:%M"),
                "data_freshness": random.choice(["Real-time", "1 hour", "Daily", "Weekly", "Stale"])
            })
        
        max_val = max(v["reported_value"] for v in dept_values)
        min_val = min(v["reported_value"] for v in dept_values)
        discrepancy = round(max_val - min_val, 2)
        
        metrics_by_dept.append({
            "metric": metric_name,
            "reported_values": dept_values,
            "max_value": max_val,
            "min_value": min_val,
            "discrepancy_range": f"{discrepancy} ({round((discrepancy/min_val * 100), 1)}% variance)",
            "consensus_value": round(sum(v["reported_value"] for v in dept_values) / len(dept_values), 2)
        })
    
    # System/source alignment issues
    data_sources = [
        {
            "system": "Google Analytics",
            "departments_using": ["Analytics", "Product"],
            "connection_status": "Connected",
            "last_sync": (datetime.now() - timedelta(hours=random.randint(0, 24))).strftime("%Y-%m-%d %H:%M"),
            "discrepancy_vs_other_sources": f"+{round(random.uniform(2, 18), 1)}%"
        },
        {
            "system": "Amplitude",
            "departments_using": ["Product", "Marketing"],
            "connection_status": "Connected",
            "last_sync": (datetime.now() - timedelta(hours=random.randint(0, 24))).strftime("%Y-%m-%d %H:%M"),
            "discrepancy_vs_other_sources": f"-{round(random.uniform(2, 15), 1)}%"
        },
        {
            "system": "Custom Dashboard (Internal DB)",
            "departments_using": ["Operations", "Finance"],
            "connection_status": "Stale",
            "last_sync": (datetime.now() - timedelta(days=random.randint(3, 8))).strftime("%Y-%m-%d %H:%M"),
            "discrepancy_vs_other_sources": f"+{round(random.uniform(8, 28), 1)}%"
        },
        {
            "system": "Mixpanel",
            "departments_using": ["Marketing"],
            "connection_status": "Connected",
            "last_sync": (datetime.now() - timedelta(hours=random.randint(0, 48))).strftime("%Y-%m-%d %H:%M"),
            "discrepancy_vs_other_sources": f"-{round(random.uniform(1, 12), 1)}%"
        }
    ]
    
    # Root cause issues
    discrepancy_causes = [
        {
            "cause": "API integration lag",
            "severity": "Critical",
            "affected_metric": "User Engagement, Error Rate",
            "affected_departments": ["Analytics", "Product"],
            "description": "Google Analytics and internal dashboard out of sync; API pulls happening on different schedules",
            "detection_date": (datetime.now() - timedelta(days=3)).strftime("%Y-%m-%d"),
            "estimated_impact": "8-15% variance in reported metrics"
        },
        {
            "cause": "Filtering discrepancy",
            "severity": "High",
            "affected_metric": "Conversion Rate, NPS Score",
            "affected_departments": ["Product", "Marketing"],
            "description": "Marketing using UTM-filtered cohorts; Product using all traffic. Different bot/spam filter rules.",
            "detection_date": (datetime.now() - timedelta(days=5)).strftime("%Y-%m-%d"),
            "estimated_impact": "5-12% variance in reported metrics"
        },
        {
            "cause": "Data warehouse refresh lag",
            "severity": "High",
            "affected_metric": "Churn Rate, User Engagement",
            "affected_departments": ["Finance", "Operations"],
            "description": "Custom dashboard pulling from data warehouse updated weekly; real-time systems updated hourly",
            "detection_date": (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d"),
            "estimated_impact": "3-10% variance depending on day of week"
        },
        {
            "cause": "Definition mismatch",
            "severity": "Medium",
            "affected_metric": "User Engagement",
            "affected_departments": ["All"],
            "description": "No agreed definition of 'active user'; some count DAU, some WAU, some MAU. NPS calculation methodology differs.",
            "detection_date": (datetime.now() - timedelta(days=10)).strftime("%Y-%m-%d"),
            "estimated_impact": "2-8% variance due to definition ambiguity"
        }
    ]
    
    # Anomalies
    anomalies = [
        {
            "type": "Custom dashboard significantly stale",
            "severity": "Critical",
            "detected_date": (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d"),
            "description": "Internal dashboard last synced 6 days ago; Finance and Operations reporting week-old data to stakeholders",
            "impact": "Finance reporting incorrect metrics to board; decisions made on outdated data",
            "affected_area": "Custom Dashboard (Internal DB)"
        },
        {
            "type": "Google Analytics event tracking broken",
            "severity": "High",
            "detected_date": (datetime.now() - timedelta(days=2)).strftime("%Y-%m-%d"),
            "description": "Custom event for error tracking disabled accidentally; Error Rate metric 40% lower than reality",
            "impact": "Product team underestimating app stability issues; hidden bug severity",
            "affected_area": "Google Analytics - Error Rate metric"
        },
        {
            "type": "UTM parameter tracking inconsistent",
            "severity": "Medium",
            "detected_date": (datetime.now() - timedelta(days=4)).strftime("%Y-%m-%d"),
            "description": "Marketing campaign IDs not always passed through to analytics; 25% of traffic unattributed",
            "impact": "Marketing attribution inflated; CAC and conversion metrics suspect",
            "affected_area": "Amplitude/Mixpanel - Conversion Rate metric"
        }
    ]
    
    return {
        "analysis_date": datetime.now().strftime("%Y-%m-%d"),
        "case_id": case.id,
        "company": case.title.split(" for ")[-1] if " for " in case.title else "Mobile App Studio",
        "metrics_by_department": metrics_by_dept,
        "data_sources": data_sources,
        "discrepancy_causes": discrepancy_causes,
        "anomalies": anomalies,
        "summary": {
            "total_metrics_analyzed": len(metric_names),
            "metrics_with_significant_variance": len([m for m in metrics_by_dept if float(m["discrepancy_range"].split()[0]) > 5]),
            "departments_affected": len(departments),
            "critical_issues": len([c for c in discrepancy_causes if c["severity"] == "Critical"]),
            "data_sources_analyzed": len(data_sources),
            "sources_with_sync_issues": len([s for s in data_sources if s["connection_status"] in ["Stale", "Error"]]),
            "highest_variance_metric": max(metrics_by_dept, key=lambda x: float(x["discrepancy_range"].split()[0]))["metric"],
            "max_variance_percent": max([float(m["discrepancy_range"].split("(")[1].split("%")[0]) for m in metrics_by_dept]),
            "key_finding": "Data infrastructure fragmented across 4+ systems with no single source of truth; requires immediate reconciliation and standardization"
        }
    }


def _generate_social_sentiment_analysis_data(case: Case) -> dict:
    """
    Generate social media sentiment and brand health analysis.
    Tracks sentiment scores, brand mentions, engagement, share of voice, and trends across platforms.
    """
    platforms = ["Twitter/X", "Instagram", "TikTok", "LinkedIn", "Facebook", "YouTube"]
    
    # Overall sentiment by platform
    platform_sentiment = []
    for platform in platforms:
        total_mentions = random.randint(500, 5000)
        positive = int(total_mentions * random.uniform(0.35, 0.70))
        negative = int(total_mentions * random.uniform(0.15, 0.35))
        neutral = total_mentions - positive - negative
        
        platform_sentiment.append({
            "platform": platform,
            "total_mentions": total_mentions,
            "positive_sentiment": positive,
            "negative_sentiment": negative,
            "neutral_sentiment": neutral,
            "positive_percent": round((positive / total_mentions * 100), 1),
            "negative_percent": round((negative / total_mentions * 100), 1),
            "sentiment_score": round((positive - negative) / total_mentions, 3),
            "engagement_rate": round(random.uniform(1.2, 8.5), 2),
            "avg_engagement": random.randint(100, 8000)
        })
    
    # Brand mention trends (30-day rolling)
    mention_trends = []
    base_mentions = random.randint(1500, 3000)
    base_sentiment = random.uniform(0.45, 0.65)
    for day in range(30):
        daily_mentions = int(base_mentions + random.uniform(-400, 600))
        daily_sentiment = round(base_sentiment + random.uniform(-0.08, 0.08), 3)
        mention_trends.append({
            "day": day + 1,
            "mentions": daily_mentions,
            "sentiment_score": daily_sentiment,
            "positive_mentions": int(daily_mentions * daily_sentiment),
            "negative_mentions": int(daily_mentions * (1 - daily_sentiment))
        })
        base_mentions = daily_mentions
        base_sentiment = daily_sentiment
    
    # Top hashtags and campaigns
    hashtags = []
    campaign_names = ["#BrandLove", "#ProductLaunch", "#CustomerStories", "#BehindTheScenes", "#Community"]
    for i, campaign in enumerate(campaign_names):
        impressions = random.randint(50000, 500000)
        engagement = random.randint(1000, 50000)
        sentiment_pos = random.uniform(0.45, 0.75)
        hashtags.append({
            "hashtag": campaign,
            "impressions": impressions,
            "engagements": engagement,
            "engagement_rate": round((engagement / impressions * 100), 2),
            "positive_sentiment": round(sentiment_pos * 100, 1),
            "negative_sentiment": round((1 - sentiment_pos) * 100, 1),
            "trend": random.choice(["Rising", "Stable", "Declining"])
        })
    
    # Share of voice (vs competitors)
    competitors = ["Competitor A", "Competitor B", "Competitor C", "Our Brand"]
    sov_data = []
    total_mentions_all = sum(p["total_mentions"] for p in platform_sentiment)
    our_mentions = total_mentions_all
    comp_mentions = [random.randint(8000, 15000) for _ in competitors[:-1]]
    
    for i, comp in enumerate(competitors):
        if comp == "Our Brand":
            mentions = our_mentions
        else:
            mentions = comp_mentions[i]
        sov_data.append({
            "brand": comp,
            "mentions": mentions,
            "share_of_voice": round((mentions / (our_mentions + sum(comp_mentions)) * 100), 1),
            "sentiment_score": round(random.uniform(0.35, 0.72), 3)
        })
    
    # Sentiment drivers (what's driving positive/negative)
    sentiment_drivers = [
        {
            "topic": "Product Quality",
            "sentiment_impact": random.choice(["Positive", "Negative"]),
            "mention_volume": random.randint(200, 1200),
            "sentiment_score": round(random.uniform(-0.3, 0.8), 2),
            "trend": random.choice(["Improving", "Declining", "Stable"])
        },
        {
            "topic": "Customer Service",
            "sentiment_impact": random.choice(["Positive", "Negative"]),
            "mention_volume": random.randint(150, 900),
            "sentiment_score": round(random.uniform(-0.5, 0.7), 2),
            "trend": random.choice(["Improving", "Declining", "Stable"])
        },
        {
            "topic": "Pricing/Value",
            "sentiment_impact": random.choice(["Positive", "Negative"]),
            "mention_volume": random.randint(180, 1100),
            "sentiment_score": round(random.uniform(-0.6, 0.5), 2),
            "trend": random.choice(["Improving", "Declining", "Stable"])
        },
        {
            "topic": "Brand Values/Ethics",
            "sentiment_impact": random.choice(["Positive", "Negative"]),
            "mention_volume": random.randint(100, 600),
            "sentiment_score": round(random.uniform(-0.4, 0.75), 2),
            "trend": random.choice(["Improving", "Declining", "Stable"])
        }
    ]
    
    # Anomalies and crises
    anomalies = [
        {
            "type": "Negative sentiment spike on TikTok",
            "severity": "High",
            "detected_date": (datetime.now() - timedelta(days=2)).strftime("%Y-%m-%d"),
            "description": "Viral complaint video about product received 2.3M views; 73% negative sentiment",
            "impact": "TikTok sentiment dropped from +0.52 to -0.28 in 48 hours; reached Gen-Z audience",
            "affected_platform": "TikTok",
            "volume": "2.3M impressions"
        },
        {
            "type": "Positive campaign momentum on Instagram",
            "severity": "Positive",
            "detected_date": (datetime.now() - timedelta(days=5)).strftime("%Y-%m-%d"),
            "description": "User-generated content campaign #BrandLove exceeded projections by 340%",
            "impact": "Instagram engagement +45%; sentiment improved from +0.48 to +0.68",
            "affected_platform": "Instagram",
            "volume": "450K engagements"
        },
        {
            "type": "Competitor sentiment overtaking ours on LinkedIn",
            "severity": "Medium",
            "detected_date": (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d"),
            "description": "Competitor B launched thought leadership campaign; share of voice grew from 22% to 31%",
            "impact": "Our brand share of voice on LinkedIn dropped from 35% to 28%",
            "affected_platform": "LinkedIn",
            "volume": "3.2K mentions"
        }
    ]
    
    # Brand health metrics
    overall_sentiment = round(sum(p["sentiment_score"] for p in platform_sentiment) / len(platform_sentiment), 3)
    
    return {
        "analysis_date": datetime.now().strftime("%Y-%m-%d"),
        "case_id": case.id,
        "company": case.title.split(" for ")[-1] if " for " in case.title else "Marketing Agency",
        "platform_sentiment": platform_sentiment,
        "mention_trends": mention_trends,
        "hashtags": hashtags,
        "share_of_voice": sov_data,
        "sentiment_drivers": sentiment_drivers,
        "anomalies": anomalies,
        "summary": {
            "overall_sentiment_score": overall_sentiment,
            "platforms_analyzed": len(platforms),
            "total_mentions_analyzed": sum(p["total_mentions"] for p in platform_sentiment),
            "positive_mentions": sum(p["positive_sentiment"] for p in platform_sentiment),
            "negative_mentions": sum(p["negative_sentiment"] for p in platform_sentiment),
            "overall_positive_percent": round(sum(p["positive_sentiment"] for p in platform_sentiment) / sum(p["total_mentions"] for p in platform_sentiment) * 100, 1),
            "overall_negative_percent": round(sum(p["negative_sentiment"] for p in platform_sentiment) / sum(p["total_mentions"] for p in platform_sentiment) * 100, 1),
            "best_platform": max(platform_sentiment, key=lambda x: x["sentiment_score"])["platform"],
            "worst_platform": min(platform_sentiment, key=lambda x: x["sentiment_score"])["platform"],
            "share_of_voice": round((our_mentions / (our_mentions + sum(comp_mentions)) * 100), 1),
            "critical_issues": len([a for a in anomalies if a["severity"] in ["High", "Critical"]]),
            "positive_opportunities": len([a for a in anomalies if a["severity"] == "Positive"]),
            "key_finding": "Brand sentiment stable overall, but platform-specific risks emerging; TikTok crisis requires immediate response"
        }
    }


def _generate_mobile_app_behavior_data(case: Case) -> dict:
    """
    Generate mobile app user behavior and feature discoverability analysis.
    Tracks feature adoption, user journeys, discoverability issues, and engagement funnels.
    """
    # App features and discovery analysis
    features = [
        "Property Search",
        "Saved Listings",
        "Virtual Tours",
        "Schedule Showings",
        "Mortgage Calculator",
        "Neighborhood Info",
        "Agent Messaging",
        "Offer Management"
    ]
    
    # Feature discovery and usage metrics
    feature_metrics = []
    total_users = 50000
    for feature in features:
        discovered = int(total_users * random.uniform(0.25, 0.85))
        used = int(discovered * random.uniform(0.30, 0.80))
        repeat_users = int(used * random.uniform(0.20, 0.70))
        dau = int(total_users * random.uniform(0.02, 0.15))
        
        discovery_rate = round((discovered / total_users * 100), 1)
        adoption_rate = round((used / discovered * 100), 1) if discovered else 0
        retention_rate = round((repeat_users / used * 100), 1) if used else 0
        
        feature_metrics.append({
            "feature": feature,
            "discovered_users": discovered,
            "active_users": used,
            "repeat_users": repeat_users,
            "daily_active_users": dau,
            "discovery_rate_percent": discovery_rate,
            "adoption_rate_percent": adoption_rate,
            "retention_rate_percent": retention_rate,
            "avg_sessions_per_user": round(random.uniform(1.2, 8.5), 1),
            "time_on_feature_minutes": round(random.uniform(2, 45), 1),
            "user_satisfaction": round(random.uniform(3.0, 4.9), 1)
        })
    
    # User behavior funnel (discover → interact → convert)
    user_funnel = []
    funnel_stages = [
        ("App Install", 50000),
        ("First Open", 50000 * random.uniform(0.85, 0.95)),
        ("Browse Features", 50000 * random.uniform(0.75, 0.88)),
        ("Discover Key Feature", 50000 * random.uniform(0.55, 0.75)),
        ("Use Feature", 50000 * random.uniform(0.35, 0.55)),
        ("Repeat Use", 50000 * random.uniform(0.15, 0.35)),
        ("Schedule Showing/Action", 50000 * random.uniform(0.05, 0.15))
    ]
    
    for i, (stage, count) in enumerate(funnel_stages):
        if i == 0:
            drop_off = 0
        else:
            drop_off = round((funnel_stages[i-1][1] - count) / funnel_stages[i-1][1] * 100, 1)
        
        user_funnel.append({
            "stage": stage,
            "users": int(count),
            "percent_of_total": round((count / funnel_stages[0][1] * 100), 1),
            "drop_off_rate": drop_off
        })
    
    # Cohort analysis - retention by user cohort
    cohorts = []
    cohort_periods = ["Week 1", "Week 2-4", "Month 2", "Month 3"]
    for cohort in cohort_periods:
        retention_d7 = round(random.uniform(0.40, 0.80), 2)
        retention_d30 = round(random.uniform(0.25, 0.65), 2)
        feature_adoption = round(random.uniform(0.30, 0.75), 2)
        
        cohorts.append({
            "cohort": cohort,
            "users": random.randint(2000, 12000),
            "retention_day_7": retention_d7,
            "retention_day_30": retention_d30,
            "key_feature_adoption": feature_adoption,
            "churn_rate": round(1 - retention_d30, 2),
            "repeat_purchase_rate": round(random.uniform(0.30, 0.70), 2)
        })
    
    # User segments by behavior
    segments = [
        {
            "segment": "High-Engagement Users",
            "size": random.randint(3000, 8000),
            "features_used": random.randint(5, 8),
            "avg_session_length": random.randint(15, 45),
            "retention_d30": round(random.uniform(0.70, 0.95), 2),
            "repeat_purchase_rate": round(random.uniform(0.60, 0.85), 2),
            "churn_risk": "Low"
        },
        {
            "segment": "Feature-Explorers",
            "size": random.randint(8000, 15000),
            "features_used": random.randint(3, 5),
            "avg_session_length": random.randint(8, 18),
            "retention_d30": round(random.uniform(0.45, 0.70), 2),
            "repeat_purchase_rate": round(random.uniform(0.35, 0.55), 2),
            "churn_risk": "Medium"
        },
        {
            "segment": "Feature-Blind Users",
            "size": random.randint(12000, 20000),
            "features_used": random.randint(1, 2),
            "avg_session_length": random.randint(2, 8),
            "retention_d30": round(random.uniform(0.15, 0.40), 2),
            "repeat_purchase_rate": round(random.uniform(0.10, 0.30), 2),
            "churn_risk": "Critical"
        }
    ]
    
    # Discoverability issues
    discoverability_issues = [
        {
            "feature": "Virtual Tours",
            "severity": "Critical",
            "discovery_rate": 28.5,
            "issue": "Hidden in secondary menu; users don't find it",
            "impact": "Only 28.5% discover; 15% adoption rate despite strong UX satisfaction",
            "recommendation": "Move to main tab; add onboarding nudge"
        },
        {
            "feature": "Mortgage Calculator",
            "severity": "High",
            "discovery_rate": 34.2,
            "issue": "Named 'Tools' but users expect 'Calculator' label",
            "impact": "34% discovery but potential 70% if better labeled",
            "recommendation": "Rename to 'Mortgage Calculator'; add icon clarity"
        },
        {
            "feature": "Agent Messaging",
            "severity": "High",
            "discovery_rate": 41.8,
            "issue": "Users expect direct contact but messaging is buried",
            "impact": "Missing engagement opportunity; high-value feature underutilized",
            "recommendation": "Highlight in property view; enable in-context access"
        },
        {
            "feature": "Neighborhood Info",
            "severity": "Medium",
            "discovery_rate": 52.3,
            "issue": "Available but not obvious as distinct feature",
            "impact": "Users missing demographic/crime/school data that drives decisions",
            "recommendation": "Make discoverable during property search flow"
        }
    ]
    
    # Churn drivers
    churn_analysis = [
        {
            "cause": "Didn't discover key feature",
            "churn_rate": round(random.uniform(0.60, 0.80), 2),
            "affected_users": random.randint(5000, 12000),
            "primary_missing_feature": "Virtual Tours / Agent Messaging"
        },
        {
            "cause": "Slow app performance",
            "churn_rate": round(random.uniform(0.50, 0.70), 2),
            "affected_users": random.randint(3000, 7000),
            "primary_missing_feature": "Property Search (load times)"
        },
        {
            "cause": "Incomplete property data",
            "churn_rate": round(random.uniform(0.55, 0.75), 2),
            "affected_users": random.randint(4000, 9000),
            "primary_missing_feature": "Neighborhood Info / Showings"
        },
        {
            "cause": "Insufficient customization",
            "churn_rate": round(random.uniform(0.45, 0.65), 2),
            "affected_users": random.randint(2000, 5000),
            "primary_missing_feature": "Saved Listings / Preferences"
        }
    ]
    
    # Anomalies
    anomalies = [
        {
            "type": "Virtual Tours feature abandoned",
            "severity": "Critical",
            "detected_date": (datetime.now() - timedelta(days=3)).strftime("%Y-%m-%d"),
            "description": "28.5% discovery rate but 0% conversion to showings; users explore but don't schedule",
            "impact": "High-intent users dropping off; missing conversion opportunity",
            "affected_segment": "Feature-Explorers"
        },
        {
            "type": "Feature-Blind cohort growing",
            "severity": "High",
            "detected_date": (datetime.now() - timedelta(days=5)).strftime("%Y-%m-%d"),
            "description": "New users spending avg 4.2 mins/session; only discovering 1.8 features before churn",
            "impact": "Onboarding not guiding feature discovery; 68% churn in 30 days",
            "affected_segment": "Week 1-2 cohorts"
        },
        {
            "type": "Repeat purchase plateauing",
            "severity": "High",
            "detected_date": (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d"),
            "description": "Repeat purchase rate declining 15.25%; users not returning after initial transaction",
            "impact": "LTV impacted; need to improve feature stickiness and engagement loops",
            "affected_segment": "All users post-transaction"
        }
    ]
    
    return {
        "analysis_date": datetime.now().strftime("%Y-%m-%d"),
        "case_id": case.id,
        "company": case.title.split(" for ")[-1] if " for " in case.title else "Real Estate Firm",
        "total_app_users": total_users,
        "feature_metrics": feature_metrics,
        "user_funnel": user_funnel,
        "cohorts": cohorts,
        "user_segments": segments,
        "discoverability_issues": discoverability_issues,
        "churn_analysis": churn_analysis,
        "anomalies": anomalies,
        "summary": {
            "total_features": len(features),
            "well_discovered_features": len([f for f in feature_metrics if f["discovery_rate_percent"] > 60]),
            "poorly_discovered_features": len([f for f in feature_metrics if f["discovery_rate_percent"] < 40]),
            "critical_discoverability_issues": len([d for d in discoverability_issues if d["severity"] == "Critical"]),
            "avg_features_per_user": round(sum(s["features_used"] for s in segments) / len(segments), 1),
            "overall_retention_d30": round(sum(c["retention_day_30"] for c in cohorts) / len(cohorts), 2),
            "overall_churn_rate": round(sum(c["churn_rate"] for c in cohorts) / len(cohorts), 2),
            "largest_at_risk_segment": max(segments, key=lambda x: x["size"] if x["churn_risk"] == "Critical" else 0)["segment"] if any(s["churn_risk"] == "Critical" for s in segments) else "N/A",
            "biggest_discovery_gap": max(discoverability_issues, key=lambda x: (70 - x["discovery_rate"]))["feature"],
            "key_finding": f"Feature discoverability broken; {len([d for d in discoverability_issues if d['severity'] in ['Critical', 'High']])} critical issues blocking engagement; Feature-Blind segment 42% of user base"
        }
    }


def _generate_marketing_attribution_quality_data(case: Case) -> dict:
    """
    Generate marketing attribution quality and data accuracy analysis.
    Identifies attribution model conflicts, UTM tracking issues, channel misattribution, and reconciliation gaps.
    """
    channels = ["Paid Search", "Social Media Ads", "Email", "Organic Search", "Direct", "Referral"]
    attribution_models = ["First-Touch", "Last-Touch", "Linear", "Time-Decay"]
    
    # Channel attribution discrepancies (same conversion, different model credit)
    channel_attribution = []
    for channel in channels:
        # Same 100 conversions, different credit by model
        attributions = {
            "channel": channel,
            "total_conversions": 100,
            "attribution_by_model": {}
        }
        
        total_credit = 0
        for i, model in enumerate(attribution_models):
            credit = round(100 * random.uniform(0.15, 0.40), 1)
            attributions["attribution_by_model"][model] = credit
            total_credit += credit
        
        # Calculate variance
        credits = list(attributions["attribution_by_model"].values())
        variance = round(max(credits) - min(credits), 1)
        
        channel_attribution.append({
            "channel": channel,
            "total_conversions": 100,
            "first_touch_credit": attributions["attribution_by_model"][attribution_models[0]],
            "last_touch_credit": attributions["attribution_by_model"][attribution_models[1]],
            "linear_credit": attributions["attribution_by_model"][attribution_models[2]],
            "time_decay_credit": attributions["attribution_by_model"][attribution_models[3]],
            "credit_variance": variance,
            "avg_credit": round(sum(credits) / len(credits), 1),
            "model_agreement": "Low" if variance > 15 else ("Medium" if variance > 8 else "High")
        })
    
    # System reconciliation issues
    data_sources = [
        {
            "system": "Google Analytics 4",
            "conversions_reported": random.randint(800, 1200),
            "attributed_to_paid": round(random.uniform(0.35, 0.55) * random.randint(800, 1200)),
            "last_updated": (datetime.now() - timedelta(hours=random.randint(0, 12))).strftime("%Y-%m-%d %H:%M"),
            "utm_tracking_coverage": round(random.uniform(0.75, 0.95), 3)
        },
        {
            "system": "Facebook Ads Manager",
            "conversions_reported": random.randint(600, 1000),
            "attributed_to_paid": random.randint(600, 1000),
            "last_updated": (datetime.now() - timedelta(hours=random.randint(0, 48))).strftime("%Y-%m-%d %H:%M"),
            "utm_tracking_coverage": round(random.uniform(0.40, 0.75), 3)
        },
        {
            "system": "CRM (Salesforce)",
            "conversions_reported": random.randint(700, 1100),
            "attributed_to_paid": round(random.uniform(0.30, 0.50) * random.randint(700, 1100)),
            "last_updated": (datetime.now() - timedelta(hours=random.randint(12, 72))).strftime("%Y-%m-%d %H:%M"),
            "utm_tracking_coverage": round(random.uniform(0.60, 0.85), 3)
        }
    ]
    
    # Calculate discrepancies
    ga_convs = data_sources[0]["conversions_reported"]
    fb_convs = data_sources[1]["conversions_reported"]
    crm_convs = data_sources[2]["conversions_reported"]
    
    max_discrepancy = round(max(ga_convs, fb_convs, crm_convs) - min(ga_convs, fb_convs, crm_convs), 0)
    
    # UTM tracking issues
    utm_issues = [
        {
            "issue": "Missing UTM parameters",
            "severity": "Critical",
            "affected_traffic_percent": round(random.uniform(15, 35), 1),
            "traffic_unattributed": random.randint(3000, 8000),
            "source": "Email campaigns, social referrals",
            "description": "Email newsletter links missing utm_source/utm_medium; social posts missing utm_campaign",
            "impact": "~25% of conversions unattributed to actual source; organic credit inflated"
        },
        {
            "issue": "UTM parameter inconsistency",
            "severity": "High",
            "affected_traffic_percent": round(random.uniform(8, 20), 1),
            "traffic_unattributed": random.randint(2000, 5000),
            "source": "Cross-team campaigns (Marketing, Comms, Fundraising)",
            "description": "Different teams using different conventions (facebook vs FB vs facebookads); utm_medium values not standardized",
            "impact": "Impossible to aggregate channel performance; same traffic counted as multiple channels"
        },
        {
            "issue": "Last-click attribution inflating Paid channels",
            "severity": "High",
            "affected_traffic_percent": round(random.uniform(20, 40), 1),
            "traffic_unattributed": random.randint(4000, 10000),
            "source": "Multi-touch journeys (organic search → paid retargeting → conversion)",
            "description": "Model defaults to last-click, giving all credit to final paid ad instead of organic discovery",
            "impact": "Paid channel ROI overstated by 40-60%; organic channel value hidden"
        }
    ]
    
    # Data pipeline anomalies
    anomalies = [
        {
            "type": "Facebook-CRM conversion mismatch",
            "severity": "Critical",
            "detected_date": (datetime.now() - timedelta(days=2)).strftime("%Y-%m-%d"),
            "description": f"Facebook reports {data_sources[1]['conversions_reported']} conversions; CRM shows only {int(data_sources[1]['conversions_reported'] * 0.65)} attributed to Facebook",
            "impact": f"${int(data_sources[1]['conversions_reported'] * 50)} in unreconciled revenue; wrong ROI calculations",
            "affected_system": "Facebook Ads Manager ↔ Salesforce"
        },
        {
            "type": "Email tracking pixel broken",
            "severity": "High",
            "detected_date": (datetime.now() - timedelta(days=5)).strftime("%Y-%m-%d"),
            "description": "Email UTM parameters present but tracking pixel inconsistent; bouncing off ESP before reaching GA",
            "impact": "Email-attributed conversions underreported by ~35%; channel ROI unknown",
            "affected_system": "Email ESP → Google Analytics"
        },
        {
            "type": "Organic search data delayed 24-48 hours",
            "severity": "Medium",
            "detected_date": (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d"),
            "description": "GA organic search data batched daily; real-time dashboard shows stale data affecting weekly reports",
            "impact": "Weekly attribution decisions made on 24-48hr old data; organic strategy lagging market trends",
            "affected_system": "Google Analytics organic data pipeline"
        }
    ]
    
    return {
        "analysis_date": datetime.now().strftime("%Y-%m-%d"),
        "case_id": case.id,
        "company": case.title.split(" for ")[-1] if " for " in case.title else "Nonprofit Organization",
        "channel_attribution_models": channel_attribution,
        "data_sources": data_sources,
        "utm_tracking_issues": utm_issues,
        "anomalies": anomalies,
        "summary": {
            "channels_analyzed": len(channels),
            "attribution_models_analyzed": len(attribution_models),
            "avg_channel_credit_variance": round(sum(c["credit_variance"] for c in channel_attribution) / len(channel_attribution), 1),
            "channels_with_low_agreement": len([c for c in channel_attribution if c["model_agreement"] == "Low"]),
            "data_sources_reconciled": len(data_sources),
            "max_conversion_discrepancy": int(max_discrepancy),
            "max_discrepancy_percent": round((max_discrepancy / min(ga_convs, fb_convs, crm_convs) * 100), 1),
            "utm_issues_identified": len(utm_issues),
            "total_unattributed_traffic": sum(u["traffic_unattributed"] for u in utm_issues),
            "critical_issues": len([a for a in anomalies if a["severity"] == "Critical"]),
            "key_finding": f"Attribution chaos: {round(sum(u['affected_traffic_percent'] for u in utm_issues) / len(utm_issues), 1)}% of traffic unattributed; {len([c for c in channel_attribution if c['credit_variance'] > 15])} channels have conflicting model attribution; systems out of sync by {int(max_discrepancy)} conversions"
        }
    }
