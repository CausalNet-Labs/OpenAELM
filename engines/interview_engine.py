"""
==============================================================================
interview_engine.py
Advanced Employment & Labor Model (AELM)
==============================================================================
"""

from dataclasses import dataclass, field
from typing import List

@dataclass
class InterviewQuestion:
    category: str
    question: str
    reason: str

@dataclass
class InterviewResult:
    screening: List[InterviewQuestion] = field(default_factory=list)
    behavioral: List[InterviewQuestion] = field(default_factory=list)
    technical: List[InterviewQuestion] = field(default_factory=list)
    weak_points: List[str] = field(default_factory=list)
    coaching: List[str] = field(default_factory=list)

class InterviewEngine:

    def evaluate(self, resume, job, match):

        result = InterviewResult()

        result.screening.extend([
            InterviewQuestion(
                "Screening",
                "Tell me about yourself.",
                "Common recruiter opener."
            ),
            InterviewQuestion(
                "Screening",
                f"Why are you interested in the {job.title or 'position'}?",
                "Motivation."
            )
        ])

        result.behavioral.extend([
            InterviewQuestion(
                "Behavioral",
                "Describe a difficult problem you solved.",
                "Problem solving."
            ),
            InterviewQuestion(
                "Behavioral",
                "Describe a time you handled conflict.",
                "Communication."
            )
        ])

        for skill in match.matched_skills[:5]:
            result.technical.append(
                InterviewQuestion(
                    "Technical",
                    f"Explain your experience with {skill}.",
                    "Validate claimed skill."
                )
            )

        for missing in match.missing_skills:
            result.weak_points.append(
                f"Be prepared to discuss exposure to '{missing}' honestly."
            )

        result.coaching.extend([
            "Use the STAR method (Situation, Task, Action, Result).",
            "Answer with specific examples from your own experience.",
            "Do not exaggerate or invent accomplishments.",
            "If you lack experience in an area, explain how related experience transfers."
        ])

        return result

def generate_interview(resume, job, match):
    return InterviewEngine().evaluate(resume, job, match)
