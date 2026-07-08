"""
==============================================================================
hire_probability.py
Advanced Employment & Labor Model (AELM)
==============================================================================
"""

from dataclasses import dataclass, field
from typing import List

@dataclass
class HireProbabilityResult:
    recruiter_pass_range: str = ""
    interview_range: str = ""
    confidence: str = ""
    competition: str = ""
    overall_score: float = 0.0
    reasoning: List[str] = field(default_factory=list)

class HireProbabilityEngine:

    def __init__(self, resume, job, match, ats):
        self.resume = resume
        self.job = job
        self.match = match
        self.ats = ats

    def evaluate(self):
        r = HireProbabilityResult()

        score = (
            self.match.semantic_score * 0.45 +
            self.ats.survivability_score * 0.55
        )

        if len(self.match.missing_skills) == 0:
            score += 5

        score = min(score, 100)
        r.overall_score = round(score, 1)

        if score >= 85:
            r.recruiter_pass_range = "80–95%"
            r.interview_range = "70–90%"
            r.confidence = "High"
            r.competition = "Medium"
        elif score >= 70:
            r.recruiter_pass_range = "60–80%"
            r.interview_range = "45–70%"
            r.confidence = "Moderate"
            r.competition = "High"
        elif score >= 55:
            r.recruiter_pass_range = "35–55%"
            r.interview_range = "20–45%"
            r.confidence = "Moderate"
            r.competition = "High"
        else:
            r.recruiter_pass_range = "5–30%"
            r.interview_range = "5–20%"
            r.confidence = "Low"
            r.competition = "High"

        r.reasoning.append(
            "Estimate is based on ATS score, semantic match, and resume/job overlap."
        )
        r.reasoning.append(
            "Competition level is a qualitative heuristic."
        )
        r.reasoning.append(
            "These estimates are not guarantees and do not use live hiring or ATS data."
        )

        return r

def estimate_hire_probability(resume, job, match, ats):
    return HireProbabilityEngine(resume, job, match, ats).evaluate()
