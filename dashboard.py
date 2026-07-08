"""
==============================================================================
dashboard.py
Advanced Employment & Labor Model (AELM)
Strategic Output Dashboard
==============================================================================
"""

from dataclasses import dataclass, field
from typing import List

@dataclass
class DashboardResult:
    ats_survivability_score: str
    hire_probability: str
    top_resume_fixes: List[str] = field(default_factory=list)
    job_risk_flags: List[str] = field(default_factory=list)
    fraud_verdict: str = ""
    entry_barriers: List[str] = field(default_factory=list)
    recommended_next_action: str = ""

class DashboardEngine:

    def build(self, ats, hire, risk, fraud, barriers):

        fixes = ats.improvements[:5] if hasattr(ats, "improvements") else []

        risk_flags = []
        if getattr(risk, "burnout_risk", "Low") != "Low":
            risk_flags.append(f"Burnout Risk: {risk.burnout_risk}")
        if getattr(risk, "ghost_job_risk", "Low") != "Low":
            risk_flags.append(f"Ghost Job Risk: {risk.ghost_job_risk}")
        if getattr(risk, "automation_risk", None):
            risk_flags.append(f"Automation Risk: {risk.automation_risk}")

        barrier_list = []
        barrier_list.append(f"Drug Test: {barriers.drug_test}")
        barrier_list.append(f"Background Check: {barriers.background_check}")
        barrier_list.append(f"License Requirement: {barriers.license_requirement}")
        barrier_list.append(f"Work Authorization: {barriers.work_authorization}")

        if ats.survivability_score >= 80:
            action = "Apply after proofreading and tailoring the resume."
        elif ats.survivability_score >= 60:
            action = "Address the recommended resume improvements before applying."
        else:
            action = "Rewrite the resume and improve keyword alignment before applying."

        return DashboardResult(
            ats_survivability_score=f"{ats.survivability_score}/100",
            hire_probability=hire.interview_range,
            top_resume_fixes=fixes,
            job_risk_flags=risk_flags,
            fraud_verdict=fraud.verdict,
            entry_barriers=barrier_list,
            recommended_next_action=action
        )

def build_dashboard(ats, hire, risk, fraud, barriers):
    return DashboardEngine().build(ats, hire, risk, fraud, barriers)

if __name__ == "__main__":
    print("Dashboard Engine Ready")
