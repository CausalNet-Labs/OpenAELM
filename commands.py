"""
==============================================================================
commands.py
Advanced Employment & Labor Model (AELM)
Command Implementations
==============================================================================
"""

from loader import load_resume, load_job
from pipeline import analyze
from session import session
from export import ExportEngine

_exporter = ExportEngine()


def load_resume_command(path: str):
    session.resume_text = load_resume(path)
    session.resume_path = path
    session.analyzed = False
    print(f"✓ Resume loaded: {path}")


def load_job_command(path: str):
    session.job_text = load_job(path)
    session.job_path = path
    session.analyzed = False
    print(f"✓ Job description loaded: {path}")


def analyze_command():
    analyze()


def dashboard_command():
    if not session.dashboard:
        print("Run 'analyze' first.")
        return

    d = session.dashboard
    print("\n" + "=" * 60)
    print("AELM STRATEGIC DASHBOARD")
    print("=" * 60)
    print(f"ATS Score: {d.ats_survivability_score}")
    print(f"Hire Probability: {d.hire_probability}")
    print(f"Fraud Verdict: {d.fraud_verdict}")
    print("\nTop Resume Fixes:")
    for item in d.top_resume_fixes:
        print(f" - {item}")
    print("\nJob Risk Flags:")
    for item in d.job_risk_flags:
        print(f" - {item}")
    print("\nRecommended Next Action:")
    print(d.recommended_next_action)
    print("=" * 60)


def export_command(fmt: str):
    if not session.dashboard:
        print("Run 'analyze' first.")
        return

    fmt = fmt.lower()

    if fmt == "txt":
        path = _exporter.export_txt(session.dashboard)
    elif fmt == "md":
        path = _exporter.export_md(session.dashboard)
    elif fmt == "json":
        path = _exporter.export_json(session.dashboard)
    else:
        print("Supported formats: txt, md, json")
        return

    print(f"✓ Exported: {path}")


def status_command():
    session.status()
