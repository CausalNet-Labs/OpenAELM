"""Analysis pipeline — orchestrates every local engine in order.

Runs entirely on the local machine: no network access, no external API.
"""

from typing import Callable, List, Tuple

from .session import session
from .parsing import parse_resume, parse_job
from .engines import (
    compare_resume_to_job,
    evaluate_ats,
    estimate_hire_probability,
    evaluate_job_risk,
    evaluate_fraud,
    evaluate_entry_barriers,
    evaluate_market_opportunities,
    generate_cover_letter,
    generate_interview,
    rewrite_resume,
    build_dashboard,
)


def analyze(progress: Callable[[str], None] = print):
    """Run the full analysis pipeline against the loaded resume and job."""
    if not session.resume_text:
        raise RuntimeError("No resume loaded. Use: load resume <file>")
    if not session.job_text:
        raise RuntimeError("No job description loaded. Use: load job <file>")

    steps: List[Tuple[str, Callable[[], None]]] = [
        ("Parsing resume", lambda: setattr(
            session, "resume", parse_resume(session.resume_text))),
        ("Parsing job description", lambda: setattr(
            session, "job", parse_job(session.job_text))),
        ("Semantic matching", lambda: setattr(
            session, "semantic",
            compare_resume_to_job(session.resume, session.job))),
        ("ATS analysis", lambda: setattr(
            session, "ats",
            evaluate_ats(session.resume, session.job, session.semantic))),
        ("Hire probability", lambda: setattr(
            session, "hire_probability",
            estimate_hire_probability(
                session.resume, session.job, session.semantic, session.ats))),
        ("Job risk analysis", lambda: setattr(
            session, "risk", evaluate_job_risk(session.job))),
        ("Fraud screening", lambda: setattr(
            session, "fraud", evaluate_fraud(session.job_text))),
        ("Entry barriers", lambda: setattr(
            session, "entry_barriers",
            evaluate_entry_barriers(session.job))),
        ("Market opportunities", lambda: setattr(
            session, "market",
            evaluate_market_opportunities(session.resume))),
        ("Cover letter", lambda: setattr(
            session, "cover_letter",
            generate_cover_letter(session.resume, session.job))),
        ("Interview prep", lambda: setattr(
            session, "interview",
            generate_interview(session.resume, session.job, session.semantic))),
        ("Resume rewrite", lambda: setattr(
            session, "rewrite",
            rewrite_resume(session.resume, session.job))),
        ("Building dashboard", lambda: setattr(
            session, "dashboard",
            build_dashboard(
                session.ats, session.hire_probability, session.risk,
                session.fraud, session.entry_barriers))),
    ]

    total = len(steps)
    for i, (label, fn) in enumerate(steps, 1):
        progress(f"[{i}/{total}] {label}...")
        fn()

    session.analyzed = True
    progress("\nAnalysis complete. Try: dashboard, ats, rewrite, "
             "coverletter, interview, export md")
    return session.dashboard
