"""Heuristic resume parser (fully local)."""

import re
from dataclasses import dataclass, field
from typing import List, Optional


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
    "python", "sql", "excel", "power bi", "tableau", "aws", "azure", "linux",
    "windows", "javascript", "java", "c++", "customer service", "sales",
    "communication", "leadership", "project management",
]

COMMON_CERTS = [
    "aws", "comptia", "security+", "network+", "cpr", "bls", "pmp",
    "scrum", "google",
]


class ResumeParser:
    def __init__(self, text: str):
        self.text = text
        self.lower = text.lower()
        self.lines = [l.strip() for l in text.splitlines() if l.strip()]
        self.resume = Resume()

    def parse(self) -> Resume:
        self._contact()
        self._summary()
        self._skills()
        self._certifications()
        self._projects()
        self._achievements()
        return self.resume

    def _contact(self) -> None:
        if self.lines:
            self.resume.name = self.lines[0]
        m = EMAIL.search(self.text)
        if m:
            self.resume.email = m.group()
        m = PHONE.search(self.text)
        if m:
            self.resume.phone = m.group()
        for line in self.lines:
            ll = line.lower()
            if "linkedin.com" in ll:
                self.resume.linkedin = line
            elif "github.com" in ll:
                self.resume.github = line

    def _is_contact_line(self, line: str) -> bool:
        return bool(EMAIL.search(line) or PHONE.search(line)) or \
            "linkedin.com" in line.lower() or "github.com" in line.lower()

    def _summary(self) -> None:
        body = [l for l in self.lines[1:] if not self._is_contact_line(l)]
        if body:
            self.resume.summary = " ".join(body[:2])

    def _skills(self) -> None:
        self.resume.skills = [
            s.title() for s in COMMON_SKILLS if s in self.lower
        ]

    def _certifications(self) -> None:
        self.resume.certifications = [
            c.upper() for c in COMMON_CERTS if c in self.lower
        ]

    def _projects(self) -> None:
        self.resume.projects = [
            l for l in self.lines if "project" in l.lower()
        ]

    def _achievements(self) -> None:
        self.resume.achievements = [
            l for l in self.lines
            if any(ch.isdigit() for ch in l) and not self._is_contact_line(l)
        ]


def parse_resume(text: str) -> Resume:
    return ResumeParser(text).parse()
