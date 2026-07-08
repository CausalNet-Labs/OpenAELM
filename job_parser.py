"""
==============================================================================
job_parser.py
Advanced Employment & Labor Model (AELM)
==============================================================================
"""

from dataclasses import dataclass, field
from typing import List, Optional
import re

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
    "python","sql","excel","aws","azure","linux","javascript","java",
    "customer service","communication","leadership","project management"
]

BENEFITS = [
    "401(k)","health insurance","dental","vision","pto","paid time off",
    "bonus","stock","tuition","remote"
]

class JobParser:

    def __init__(self, text:str):
        self.text=text
        self.lower=text.lower()
        self.lines=[l.strip() for l in text.splitlines() if l.strip()]
        self.job=JobDescription()

    def parse(self):
        self.parse_title()
        self.parse_work_type()
        self.parse_salary()
        self.parse_experience()
        self.parse_education()
        self.parse_skills()
        self.parse_benefits()
        self.parse_compliance()
        self.parse_risks()
        self.parse_fraud()
        self.parse_responsibilities()
        return self.job

    def parse_title(self):
        if self.lines:
            self.job.title=self.lines[0]

    def parse_work_type(self):
        if "remote" in self.lower:
            self.job.work_type="Remote"
        elif "hybrid" in self.lower:
            self.job.work_type="Hybrid"
        else:
            self.job.work_type="On-site"

    def parse_salary(self):
        m=re.search(r"\$[\d,]+(?:\s*-\s*\$?[\d,]+)?",self.text)
        if m:
            self.job.salary=m.group()

    def parse_experience(self):
        m=re.search(r"(\d+\+?\s*(?:years?|yrs?))",self.lower)
        if m:
            self.job.experience_required=m.group(1)

    def parse_education(self):
        for item in ["bachelor","master","associate","high school","ged"]:
            if item in self.lower:
                self.job.education_required.append(item.title())

    def parse_skills(self):
        for skill in SKILLS:
            if skill in self.lower:
                self.job.required_skills.append(skill.title())

    def parse_benefits(self):
        for b in BENEFITS:
            if b.lower() in self.lower:
                self.job.benefits.append(b)

    def parse_compliance(self):
        checks={
            "background":"Background Check",
            "drug test":"Drug Test",
            "e-verify":"E-Verify",
            "security clearance":"Security Clearance",
            "work authorization":"Work Authorization"
        }
        for k,v in checks.items():
            if k in self.lower:
                self.job.compliance.append(v)

    def parse_risks(self):
        flags={
            "fast-paced":"Burnout Risk",
            "wear many hats":"Role Creep",
            "always hiring":"Ghost Job Indicator",
            "weekends":"Weekend Work",
            "overtime":"Overtime Expected"
        }
        for k,v in flags.items():
            if k in self.lower:
                self.job.risk_flags.append(v)

    def parse_fraud(self):
        fraud={
            "pay for training":"Upfront Payment",
            "gift card":"Gift Card Scam",
            "telegram":"Telegram Recruiting",
            "bitcoin":"Crypto Payment",
            "western union":"Money Transfer"
        }
        for k,v in fraud.items():
            if k in self.lower:
                self.job.fraud_flags.append(v)

    def parse_responsibilities(self):
        verbs=("develop","manage","support","design","coordinate","assist","lead","maintain","analyze")
        for line in self.lines:
            if any(v in line.lower() for v in verbs):
                self.job.responsibilities.append(line)

def parse_job(text:str)->JobDescription:
    return JobParser(text).parse()
