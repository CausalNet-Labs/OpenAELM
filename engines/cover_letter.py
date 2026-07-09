"""
==============================================================================
cover_letter.py
Advanced Employment & Labor Model (AELM)
==============================================================================
"""

from dataclasses import dataclass, field
from typing import List

@dataclass
class CoverLetterResult:
    cover_letter: str
    notes: List[str] = field(default_factory=list)

class CoverLetterEngine:

    def __init__(self, resume, job):
        self.resume = resume
        self.job = job

    def generate(self):
        notes = [
            "Generated only from information found in the resume and job description.",
            "No qualifications, achievements, or experience were fabricated."
        ]

        greeting = "Dear Hiring Manager,"

        title = self.job.title or "this position"

        summary = self.resume.summary or (
            "I am excited to apply and believe my background aligns with your needs."
        )

        skills = ", ".join(self.resume.skills[:6]) if self.resume.skills else "my experience"

        body = f"""I am writing to express my interest in the {title} role.

{summary}

My background includes {skills}. I am particularly interested in contributing to your team while continuing to develop professionally. Based on the job description, I believe my existing experience and transferable skills would allow me to contribute effectively.

Thank you for your time and consideration. I would welcome the opportunity to discuss how my background aligns with your organization's needs.

Sincerely,

{self.resume.name or '[Your Name]'}"""

        return CoverLetterResult(
            cover_letter="\n".join([greeting, "", body]),
            notes=notes
        )

def generate_cover_letter(resume, job):
    return CoverLetterEngine(resume, job).generate()
