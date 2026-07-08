"""
==============================================================================
fraud_detection.py
Advanced Employment & Labor Model (AELM)
==============================================================================
"""

from dataclasses import dataclass, field
from typing import List

@dataclass
class FraudResult:
    verdict: str = "Low Risk"
    risk_score: int = 0
    flags: List[str] = field(default_factory=list)
    verification_steps: List[str] = field(default_factory=list)
    warning: str = ""

class FraudDetectionEngine:

    RULES = {
        "pay for training": ("Requests upfront payment", 40),
        "gift card": ("Gift card request", 50),
        "bitcoin": ("Cryptocurrency payment", 50),
        "western union": ("Money transfer request", 50),
        "telegram": ("Recruitment moved to Telegram", 20),
        "wire money": ("Wire transfer request", 50),
        "send your ssn": ("Requests SSN before offer", 45),
        "bank account": ("Requests banking details early", 45),
        "check deposit": ("Check-cashing scheme", 60),
        "buy equipment": ("Purchase equipment yourself", 40),
    }

    def evaluate(self, text: str) -> FraudResult:
        result = FraudResult()
        lower = text.lower()

        for phrase, (flag, points) in self.RULES.items():
            if phrase in lower:
                result.flags.append(flag)
                result.risk_score += points

        if result.risk_score >= 70:
            result.verdict = "High Risk — Likely Scam"
            result.warning = (
                "Do not send money, financial information, identity documents, "
                "or banking details."
            )
        elif result.risk_score >= 25:
            result.verdict = "Some Caution Warranted"
        else:
            result.verdict = "Low Risk"

        result.verification_steps.extend([
            "Verify the company on its official website.",
            "Confirm the recruiter's email domain matches the company.",
            "Search the recruiter and company independently.",
            "Never pay for training, equipment, or onboarding.",
            "Treat this as a heuristic assessment, not a verified determination."
        ])

        return result

def evaluate_fraud(text: str) -> FraudResult:
    return FraudDetectionEngine().evaluate(text)

if __name__ == "__main__":
    sample = "Interview on Telegram. Buy equipment and send your SSN."
    print(evaluate_fraud(sample))
