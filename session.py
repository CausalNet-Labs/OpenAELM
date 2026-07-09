"""In-memory session state shared across commands."""

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
    rewrite: Any = None
    dashboard: Any = None

    # Runtime
    conversation: List[Dict[str, str]] = field(default_factory=list)
    analyzed: bool = False

    def clear_results(self) -> None:
        self.semantic = None
        self.ats = None
        self.hire_probability = None
        self.risk = None
        self.fraud = None
        self.entry_barriers = None
        self.market = None
        self.cover_letter = None
        self.interview = None
        self.rewrite = None
        self.dashboard = None
        self.analyzed = False

    def clear_all(self) -> None:
        self.__dict__.update(Session().__dict__)

    def status_lines(self) -> List[str]:
        return [
            f"Resume loaded : {bool(self.resume_text)}"
            + (f"  ({self.resume_path})" if self.resume_path else ""),
            f"Job loaded    : {bool(self.job_text)}"
            + (f"  ({self.job_path})" if self.job_path else ""),
            f"Analyzed      : {self.analyzed}",
            f"Chat messages : {len(self.conversation)}",
        ]


session = Session()
