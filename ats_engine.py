"""
==============================================================================
ats_engine.py
Advanced Employment & Labor Model (AELM)
==============================================================================
"""

from dataclasses import dataclass, field
from typing import List

@dataclass
class ATSResult:
    survivability_score: float = 0.0
    keyword_coverage: float = 0.0
    formatting_score: float = 100.0
    section_score: float = 100.0
    strengths: List[str] = field(default_factory=list)
    improvements: List[str] = field(default_factory=list)
    verdict: str = ""

class ATSEngine:

    def __init__(self, resume, job, match):
        self.resume = resume
        self.job = job
        self.match = match

    def evaluate(self):
        r = ATSResult()

        r.keyword_coverage = self.match.keyword_overlap

        fmt = 100
        if not self.resume.email:
            fmt -= 10
            r.improvements.append("Add an email address.")
        if not self.resume.phone:
            fmt -= 10
            r.improvements.append("Add a phone number.")
        if not self.resume.summary:
            fmt -= 5
            r.improvements.append("Add a professional summary.")
        if len(self.resume.skills) < 5:
            fmt -= 10
            r.improvements.append("Expand the skills section.")
        if not self.resume.experience:
            fmt -= 25
            r.improvements.append("Add work experience.")

        r.formatting_score = max(fmt, 0)

        score = (
            r.keyword_coverage * 0.6 +
            r.formatting_score * 0.25 +
            r.section_score * 0.15
        )

        r.survivability_score = round(min(score, 100), 1)

        if self.match.matched_skills:
            r.strengths.append(
                f"{len(self.match.matched_skills)} required skills matched."
            )

        if self.match.missing_skills:
            r.improvements.append(
                "Mirror truthful employer keywords where applicable."
            )
            r.improvements.append(
                "Address missing required skills if genuinely possessed."
            )

        if r.survivability_score >= 85:
            r.verdict = "Excellent ATS compatibility."
        elif r.survivability_score >= 70:
            r.verdict = "Strong ATS compatibility."
        elif r.survivability_score >= 55:
            r.verdict = "Moderate ATS compatibility."
        else:
            r.verdict = "Low ATS compatibility. Resume rewrite recommended."

        return r

def evaluate_ats(resume, job, match):
    return ATSEngine(resume, job, match).evaluate()
