"""
==============================================================================
resume_rewriter.py
Advanced Employment & Labor Model (AELM)
==============================================================================
"""

from dataclasses import dataclass
from typing import List

@dataclass
class RewriteResult:
    resume_text: str
    mode: str
    notes: List[str]

class ResumeRewriter:

    MODES = {
        "ats": "ATS Optimized",
        "minimal": "Minimal Edit",
        "executive": "Executive",
        "entry": "Entry Level",
        "plain": "Plain Text"
    }

    def __init__(self, resume, job=None):
        self.resume = resume
        self.job = job

    def rewrite(self, mode="ats"):
        notes = [
            "Only information found in the original resume was used.",
            "No experience, metrics, or credentials were invented."
        ]

        lines = []

        if self.resume.name:
            lines.append(self.resume.name)
        contact = " | ".join(filter(None, [
            self.resume.email,
            self.resume.phone,
            self.resume.linkedin,
            self.resume.github
        ]))
        if contact:
            lines.append(contact)

        if self.resume.summary:
            lines.extend(["", "PROFESSIONAL SUMMARY", self.resume.summary])

        if self.resume.skills:
            skills = sorted(set(self.resume.skills))
            if self.job:
                wanted = [s for s in skills if s in self.job.required_skills]
                other = [s for s in skills if s not in wanted]
                skills = wanted + other
            lines.extend(["", "SKILLS", ", ".join(skills)])

        if self.resume.certifications:
            lines.extend([
                "",
                "CERTIFICATIONS",
                *self.resume.certifications
            ])

        if self.resume.projects:
            lines.extend(["", "PROJECTS"])
            lines.extend(f"• {p}" for p in self.resume.projects)

        if self.resume.achievements:
            lines.extend(["", "ACHIEVEMENTS"])
            lines.extend(f"• {a}" for a in self.resume.achievements)

        text = "\n".join(lines)

        if mode == "plain":
            text = text.replace("• ", "- ")

        return RewriteResult(
            resume_text=text,
            mode=self.MODES.get(mode, "ATS Optimized"),
            notes=notes
        )

def rewrite_resume(resume, job=None, mode="ats"):
    return ResumeRewriter(resume, job).rewrite(mode)
