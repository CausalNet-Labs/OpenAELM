"""
==============================================================================
resume_parser.py
Advanced Employment & Labor Model (AELM)
==============================================================================
"""

from dataclasses import dataclass, field
from typing import List, Optional
import re

@dataclass
class Experience:
    title: Optional[str] = None
    company: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    bullets: List[str] = field(default_factory=list)

@dataclass
class Education:
    school: Optional[str] = None
    degree: Optional[str] = None
    graduation: Optional[str] = None

@dataclass
class Resume:
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    location: Optional[str] = None
    linkedin: Optional[str] = None
    github: Optional[str] = None
    summary: Optional[str] = None
    skills: List[str] = field(default_factory=list)
    certifications: List[str] = field(default_factory=list)
    education: List[Education] = field(default_factory=list)
    experience: List[Experience] = field(default_factory=list)
    projects: List[str] = field(default_factory=list)
    achievements: List[str] = field(default_factory=list)

EMAIL = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
PHONE = re.compile(r"(?:\+?1[\s.-]?)?(?:\(?\d{3}\)?[\s.-]?)\d{3}[\s.-]?\d{4}")

COMMON_SKILLS = [
    "python","sql","excel","power bi","tableau","aws","azure","linux",
    "windows","javascript","java","c++","customer service","sales",
    "communication","leadership","project management"
]

COMMON_CERTS = [
    "aws","comptia","security+","network+","cpr","bls","pmp","scrum","google"
]

class ResumeParser:

    def __init__(self, text:str):
        self.text=text
        self.lower=text.lower()
        self.lines=[l.strip() for l in text.splitlines() if l.strip()]
        self.resume=Resume()

    def parse(self):
        self._contact()
        self._summary()
        self._skills()
        self._certifications()
        self._projects()
        self._achievements()
        return self.resume

    def _contact(self):
        if self.lines:
            self.resume.name=self.lines[0]

        m=EMAIL.search(self.text)
        if m:
            self.resume.email=m.group()

        m=PHONE.search(self.text)
        if m:
            self.resume.phone=m.group()

        for line in self.lines:
            ll=line.lower()
            if "linkedin.com" in ll:
                self.resume.linkedin=line
            elif "github.com" in ll:
                self.resume.github=line

    def _summary(self):
        if len(self.lines)>3:
            self.resume.summary=" ".join(self.lines[1:4])

    def _skills(self):
        for skill in COMMON_SKILLS:
            if skill in self.lower:
                self.resume.skills.append(skill.title())

    def _certifications(self):
        for cert in COMMON_CERTS:
            if cert in self.lower:
                self.resume.certifications.append(cert.upper())

    def _projects(self):
        for line in self.lines:
            if "project" in line.lower():
                self.resume.projects.append(line)

    def _achievements(self):
        for line in self.lines:
            if any(ch.isdigit() for ch in line):
                self.resume.achievements.append(line)

def parse_resume(text:str)->Resume:
    return ResumeParser(text).parse()

if __name__=="__main__":
    sample="""
Jane Doe
jane@example.com
555-555-1234
Python SQL AWS Project Management
AWS Certified Cloud Practitioner
Increased productivity by 20%.
"""
    print(parse_resume(sample))
