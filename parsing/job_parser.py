"""Heuristic job-description parser (fully local)."""

import re
from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class JobDescription:
    title: Optional[str] = None
    company: Optional[str] = None
    location: Optional[str] = None
    work_type: Optional[str] = None
    employment_type: Optional[str] = None
    salary: Optional[str] = None
    experience_required: Optional[str] = None
    education_required: List[str] = field(default_factory=list)
    required_skills: List[str] = field(default_factory=list)
    preferred_skills: List[str] = field(default_factory=list)
    certifications: List[str] = field(default_factory=list)
    responsibilities: List[str] = field(default_factory=list)
    benefits: List[str] = field(default_factory=list)
    compliance: List[str] = field(default_factory=list)
    risk_flags: List[str] = field(default_factory=list)
    fraud_flags: List[str] = field(default_factory=list)


SKILLS = [
    "python", "sql", "excel", "aws", "azure", "linux", "javascript", "java",
    "customer service", "communication", "leadership", "project management",
]

BENEFITS = [
    "401(k)", "health insurance", "dental", "vision", "pto", "paid time off",
    "bonus", "stock", "tuition", "remote",
]

COMPLIANCE = {
    "background": "Background Check",
    "drug test": "Drug Test",
    "e-verify": "E-Verify",
    "security clearance": "Security Clearance",
    "work authorization": "Work Authorization",
}

RISKS = {
    "fast-paced": "Burnout Risk",
    "wear many hats": "Role Creep",
    "always hiring": "Ghost Job Indicator",
    "weekends": "Weekend Work",
    "overtime": "Overtime Expected",
}

FRAUD = {
    "pay for training": "Upfront Payment",
    "gift card": "Gift Card Scam",
    "telegram": "Telegram Recruiting",
    "bitcoin": "Crypto Payment",
    "western union": "Money Transfer",
}

RESPONSIBILITY_VERBS = (
    "develop", "manage", "support", "design", "coordinate",
    "assist", "lead", "maintain", "analyze",
)


class JobParser:
    def __init__(self, text: str):
        self.text = text
        self.lower = text.lower()
        self.lines = [l.strip() for l in text.splitlines() if l.strip()]
        self.job = JobDescription()

    def parse(self) -> JobDescription:
        j, low = self.job, self.lower

        if self.lines:
            j.title = self.lines[0]

        if "remote" in low:
            j.work_type = "Remote"
        elif "hybrid" in low:
            j.work_type = "Hybrid"
        else:
            j.work_type = "On-site"

        m = re.search(r"\$[\d,]+(?:\s*-\s*\$?[\d,]+)?", self.text)
        if m:
            j.salary = m.group()
        m = re.search(r"(\d+\+?\s*(?:years?|yrs?))", low)
        if m:
            j.experience_required = m.group(1)

        j.education_required = [
            e.title() for e in
            ("bachelor", "master", "associate", "high school", "ged")
            if e in low
        ]
        j.required_skills = [s.title() for s in SKILLS if s in low]
        j.benefits = [b for b in BENEFITS if b.lower() in low]
        j.compliance = [v for k, v in COMPLIANCE.items() if k in low]
        j.risk_flags = [v for k, v in RISKS.items() if k in low]
        j.fraud_flags = [v for k, v in FRAUD.items() if k in low]
        j.responsibilities = [
            l for l in self.lines
            if any(v in l.lower() for v in RESPONSIBILITY_VERBS)
        ]
        return j


def parse_job(text: str) -> JobDescription:
    return JobParser(text).parse()
