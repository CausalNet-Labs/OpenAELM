"""
==============================================================================
entry_barriers.py
Advanced Employment & Labor Model (AELM)
==============================================================================
"""

from dataclasses import dataclass, field
from typing import List

@dataclass
class EntryBarrierResult:
    drug_test: str = "Possible"
    background_check: str = "Possible"
    license_requirement: str = "Unlikely"
    work_authorization: str = "Possible"
    compliance_intensity: str = "Medium"
    barriers: List[str] = field(default_factory=list)
    notes: List[str] = field(default_factory=list)

class EntryBarrierEngine:

    def evaluate(self, job):
        r = EntryBarrierResult()
        text = " ".join(job.compliance + job.responsibilities).lower()

        if "drug test" in text:
            r.drug_test = "Likely"
            r.barriers.append("Drug test mentioned")
        elif any(x in (job.title or "").lower() for x in
                 ["driver","warehouse","health","medical","nurse","security"]):
            r.drug_test = "Likely"

        if "background" in text:
            r.background_check = "Likely"
            r.barriers.append("Background check mentioned")

        if "security clearance" in text:
            r.compliance_intensity = "High"
            r.barriers.append("Security clearance")

        if "work authorization" in text or "e-verify" in text:
            r.work_authorization = "Likely"
            r.barriers.append("Work authorization verification")

        if any(x in text for x in ["license","licensed","certification"]):
            r.license_requirement = "Possible"
            r.barriers.append("License/certification referenced")

        r.notes.append(
            "These are heuristic estimates based on typical hiring patterns and the job posting."
        )

        return r

def evaluate_entry_barriers(job):
    return EntryBarrierEngine().evaluate(job)
