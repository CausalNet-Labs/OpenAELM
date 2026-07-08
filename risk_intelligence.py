"""
==============================================================================
risk_intelligence.py
Advanced Employment & Labor Model (AELM)
==============================================================================
"""

from dataclasses import dataclass, field
from typing import List

@dataclass
class RiskResult:
    burnout_risk: str = "Low"
    ghost_job_risk: str = "Low"
    layoff_risk: str = "Unknown"
    automation_risk: str = "Unknown"
    flags: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)

class RiskIntelligenceEngine:

    BURNOUT = {
        "fast-paced":"Fast-paced environment",
        "wear many hats":"Role creep",
        "must thrive under pressure":"High-pressure culture",
        "overtime":"Overtime expected",
        "weekends":"Weekend work"
    }

    GHOST = {
        "always hiring":"Always hiring",
        "continuous openings":"Continuous openings",
        "pipeline":"Pipeline recruiting"
    }

    AUTOMATION = {
        "data entry":"High",
        "customer service":"Medium",
        "administrative":"High",
        "software engineer":"Low",
        "electrician":"Low"
    }

    def evaluate(self, job):
        r = RiskResult()
        text = " ".join(job.responsibilities + job.risk_flags).lower()

        burn = 0
        for k,v in self.BURNOUT.items():
            if k in text:
                burn += 1
                r.flags.append(v)

        if burn >= 3:
            r.burnout_risk = "High"
        elif burn >= 1:
            r.burnout_risk = "Medium"

        ghost = 0
        for k,v in self.GHOST.items():
            if k in text:
                ghost += 1
                r.flags.append(v)

        if ghost >= 2:
            r.ghost_job_risk = "High"
        elif ghost == 1:
            r.ghost_job_risk = "Medium"

        title = (job.title or "").lower()
        r.automation_risk = "Medium"
        for k,v in self.AUTOMATION.items():
            if k in title:
                r.automation_risk = v

        if "startup" in text:
            r.layoff_risk = "Medium"
        elif "restructuring" in text:
            r.layoff_risk = "High"

        r.recommendations.append(
            "Risk levels are heuristic estimates based on job posting language."
        )

        if r.burnout_risk != "Low":
            r.recommendations.append(
                "Ask about workload, staffing levels, and work-life balance during interviews."
            )

        return r

def evaluate_job_risk(job):
    return RiskIntelligenceEngine().evaluate(job)
