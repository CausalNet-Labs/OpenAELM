"""
==============================================================================
market_opportunity.py
Advanced Employment & Labor Model (AELM)
==============================================================================
"""

from dataclasses import dataclass, field
from typing import List

@dataclass
class Opportunity:
    title: str
    reason: str
    estimated_fit: str

@dataclass
class MarketOpportunityResult:
    opportunities: List[Opportunity] = field(default_factory=list)
    notes: List[str] = field(default_factory=list)

ROLE_MAP = {
    "Customer Service":[
        ("Call Center Representative","Strong communication overlap","High"),
        ("Client Support Specialist","Transferable support skills","High"),
        ("Patient Services Representative","Customer-facing experience","Medium")
    ],
    "Python":[
        ("Python Developer","Programming overlap","High"),
        ("Automation Specialist","Automation experience","Medium"),
        ("Data Analyst","Python commonly used","Medium")
    ],
    "SQL":[
        ("Data Analyst","Database skills","High"),
        ("Business Intelligence Analyst","Query experience","Medium")
    ],
    "Project Management":[
        ("Project Coordinator","Leadership and organization","High"),
        ("Operations Coordinator","Planning skills","Medium")
    ]
}

class MarketOpportunityEngine:

    def evaluate(self, resume):
        result = MarketOpportunityResult()
        seen = set()

        for skill in resume.skills:
            for role in ROLE_MAP.get(skill, []):
                title, reason, fit = role
                if title not in seen:
                    seen.add(title)
                    result.opportunities.append(
                        Opportunity(title, reason, fit)
                    )

        if not result.opportunities:
            result.notes.append(
                "Not enough structured skill data to recommend adjacent roles."
            )
        else:
            result.notes.append(
                "Recommendations are based only on skills found in the resume."
            )
            result.notes.append(
                "No qualifications or experience were inferred."
            )

        return result

def evaluate_market_opportunities(resume):
    return MarketOpportunityEngine().evaluate(resume)
