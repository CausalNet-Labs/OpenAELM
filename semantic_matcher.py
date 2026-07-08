"""
==============================================================================
semantic_matcher.py
Advanced Employment & Labor Model (AELM)
==============================================================================
"""

from dataclasses import dataclass, field
from typing import List, Set

@dataclass
class MatchResult:
    resume_skills: List[str] = field(default_factory=list)
    required_skills: List[str] = field(default_factory=list)
    matched_skills: List[str] = field(default_factory=list)
    missing_skills: List[str] = field(default_factory=list)
    transferable_skills: List[str] = field(default_factory=list)
    keyword_overlap: float = 0.0
    semantic_score: float = 0.0
    notes: List[str] = field(default_factory=list)

class SemanticMatcher:

    TRANSFERABLE = {
        "Customer Service":["Communication","Problem Solving"],
        "Sales":["Negotiation","Communication"],
        "Project Management":["Leadership","Communication"],
        "Excel":["Data Analysis"],
        "Python":["Automation","Scripting"],
        "SQL":["Data Analysis"]
    }

    def __init__(self,resume,job):
        self.resume=resume
        self.job=job

    def compare(self)->MatchResult:
        result=MatchResult()

        r=set(map(str.title,self.resume.skills))
        j=set(map(str.title,self.job.required_skills))

        result.resume_skills=sorted(r)
        result.required_skills=sorted(j)
        result.matched_skills=sorted(r & j)
        result.missing_skills=sorted(j - r)

        total=max(len(j),1)
        result.keyword_overlap=round(len(result.matched_skills)/total*100,1)

        transfer=[]
        for skill in r:
            transfer.extend(self.TRANSFERABLE.get(skill,[]))
        result.transferable_skills=sorted(set(transfer))

        score=result.keyword_overlap

        if len(result.missing_skills)==0:
            score+=10
            result.notes.append("All required keywords detected.")
        else:
            result.notes.append(
                f"{len(result.missing_skills)} required skills missing."
            )

        score=min(score,100)
        result.semantic_score=round(score,1)

        if score>=85:
            result.notes.append("Excellent semantic alignment.")
        elif score>=70:
            result.notes.append("Strong alignment.")
        elif score>=50:
            result.notes.append("Moderate alignment.")
        else:
            result.notes.append("Weak alignment. Resume rewrite recommended.")

        return result

def compare_resume_to_job(resume,job):
    return SemanticMatcher(resume,job).compare()
