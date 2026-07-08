"""
==============================================================================
session.py
Advanced Employment & Labor Model (AELM)
Session Manager
==============================================================================
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class Session:
    # Raw inputs
    resume_text: Optional[str] = None
    job_text: Optional[str] = None
    resume_path: Optional[str] = None
    job_path: Optional[str] = None

    # Parsed objects
    resume: Any = None
    job: Any = None

    # Analysis results
    semantic: Any = None
    ats: Any = None
    hire_probability: Any = None
    risk: Any = None
    fraud: Any = None
    entry_barriers: Any = None
    market: Any = None
    cover_letter: Any = None
    interview: Any = None
    dashboard: Any = None

    # Runtime
    conversation: List[Dict[str, str]] = field(default_factory=list)
    exports: Dict[str, str] = field(default_factory=dict)
    analyzed: bool = False

    def clear_resume(self):
        self.resume_text = None
        self.resume_path = None
        self.resume = None
        self._clear_results()

    def clear_job(self):
        self.job_text = None
        self.job_path = None
        self.job = None
        self._clear_results()

    def _clear_results(self):
        self.semantic = None
        self.ats = None
        self.hire_probability = None
        self.risk = None
        self.fraud = None
        self.entry_barriers = None
        self.market = None
        self.cover_letter = None
        self.interview = None
        self.dashboard = None
        self.analyzed = False

    def clear_all(self):
        self.__dict__.update(Session().__dict__)

    def status(self):
        print("=" * 40)
        print("AELM SESSION")
        print("=" * 40)
        print(f"Resume Loaded : {self.resume_text is not None}")
        print(f"Job Loaded    : {self.job_text is not None}")
        print(f"Analyzed      : {self.analyzed}")
        print(f"Conversation  : {len(self.conversation)} messages")
        print("=" * 40)


session = Session()
