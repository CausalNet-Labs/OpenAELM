"""AELM interactive terminal interface.

One CLI, one entry point. All commands work fully offline except
'chat', which is optional and clearly marked.
"""

import sys

from .config import CONFIG, BANNER
from .session import session
from .parsing import load_file
from .pipeline import analyze
from .engines import rewrite_resume
from .export import ExportEngine
from .llm import chat, chat_available

HELP_TEXT = """
Commands
--------
  load resume <file>    Load a resume (.txt .md .pdf .docx)
  load job <file>       Load a job description
  analyze               Run the full local analysis pipeline
  dashboard             Strategic dashboard summary
  ats                   ATS survivability details
  rewrite [mode]        Truthful resume rewrite (ats|minimal|plain)
  coverletter           Generated cover letter
  interview             Interview preparation questions
  market                Adjacent role recommendations
  risk                  Job risk + fraud details
  export <txt|md|json>  Export the dashboard to a file
  status                Show session state
  clear                 Clear session (results + chat memory)
  config                Show configuration
  version               Show version
  chat <message>        Optional LLM chat (requires AELM_HF_TOKEN)
  help                  Show this menu
  exit                  Quit
"""


def _require_analysis() -> bool:
    if not session.analyzed:
        print("Run 'analyze' first (after loading a resume and a job).")
        return False
    return True


# ---------------------------------------------------------------- commands

def cmd_load(args):
    if len(args) < 2 or args[0].lower() not in ("resume", "job"):
        print("Usage: load resume <file>  |  load job <file>")
        return
    target, path = args[0].lower(), " ".join(args[1:])
    text = load_file(path)
    if target == "resume":
        session.resume_text, session.resume_path = text, path
    else:
        session.job_text, session.job_path = text, path
    session.clear_results()
    print(f"Loaded {target}: {path} ({len(text)} chars)")


def cmd_analyze(_):
    analyze()


def cmd_dashboard(_):
    if not _require_analysis():
        return
    d = session.dashboard
    print("\n" + "=" * 60)
    print("AELM STRATEGIC DASHBOARD")
    print("=" * 60)
    print(f"ATS Score        : {d.ats_survivability_score}")
    print(f"Hire Probability : {d.hire_probability}")
    print(f"Fraud Verdict    : {d.fraud_verdict}")
    print("\nTop Resume Fixes:")
    for item in d.top_resume_fixes or ["(none)"]:
        print(f"  - {item}")
    print("\nJob Risk Flags:")
    for item in d.job_risk_flags or ["(none)"]:
        print(f"  - {item}")
    print("\nEntry Barriers:")
    for item in d.entry_barriers:
        print(f"  - {item}")
    print(f"\nRecommended Next Action:\n  {d.recommended_next_action}")
    print("=" * 60)


def cmd_ats(_):
    if not _require_analysis():
        return
    a = session.ats
    print(f"\nATS Survivability : {a.survivability_score}/100")
    print(f"Keyword Coverage  : {a.keyword_coverage}%")
    print(f"Formatting Score  : {a.formatting_score}/100")
    print(f"Verdict           : {a.verdict}")
    if a.strengths:
        print("\nStrengths:")
        for s in a.strengths:
            print(f"  - {s}")
    if a.improvements:
        print("\nImprovements:")
        for s in a.improvements:
            print(f"  - {s}")
    print()


def cmd_rewrite(args):
    if not _require_analysis():
        return
    mode = args[0].lower() if args else "ats"
    result = rewrite_resume(session.resume, session.job, mode)
    session.rewrite = result
    print(f"\n--- Rewritten Resume ({result.mode}) ---\n")
    print(result.resume_text)
    print("\nNotes:")
    for n in result.notes:
        print(f"  - {n}")
    print()


def cmd_coverletter(_):
    if not _require_analysis():
        return
    c = session.cover_letter
    print("\n--- Cover Letter ---\n")
    print(c.cover_letter)
    print("\nNotes:")
    for n in c.notes:
        print(f"  - {n}")
    print()


def cmd_interview(_):
    if not _require_analysis():
        return
    iv = session.interview
    for group, items in (
        ("Screening", iv.screening),
        ("Behavioral", iv.behavioral),
        ("Technical", iv.technical),
    ):
        if items:
            print(f"\n{group} Questions:")
            for q in items:
                print(f"  - {q.question}  ({q.reason})")
    if iv.weak_points:
        print("\nWeak Points to Prepare:")
        for w in iv.weak_points:
            print(f"  - {w}")
    print("\nCoaching:")
    for c in iv.coaching:
        print(f"  - {c}")
    print()


def cmd_market(_):
    if not _require_analysis():
        return
    m = session.market
    if m.opportunities:
        print("\nAdjacent Role Opportunities:")
        for o in m.opportunities:
            print(f"  - {o.title} [{o.estimated_fit} fit] — {o.reason}")
    for n in m.notes:
        print(f"  ({n})")
    print()


def cmd_risk(_):
    if not _require_analysis():
        return
    r, f = session.risk, session.fraud
    print(f"\nBurnout Risk    : {r.burnout_risk}")
    print(f"Ghost Job Risk  : {r.ghost_job_risk}")
    print(f"Layoff Risk     : {r.layoff_risk}")
    print(f"Automation Risk : {r.automation_risk}")
    if r.flags:
        print("Risk Flags:")
        for x in r.flags:
            print(f"  - {x}")
    print(f"\nFraud Verdict   : {f.verdict} (score {f.risk_score})")
    if f.flags:
        print("Fraud Flags:")
        for x in f.flags:
            print(f"  - {x}")
    if f.warning:
        print(f"WARNING: {f.warning}")
    print("\nVerification Steps:")
    for s in f.verification_steps:
        print(f"  - {s}")
    print()


def cmd_export(args):
    if not _require_analysis():
        return
    if len(args) != 1:
        print("Usage: export <txt|md|json>")
        return
    path = ExportEngine().export(args[0], session.dashboard)
    print(f"Exported: {path}")


def cmd_status(_):
    print("\n".join(session.status_lines()))


def cmd_clear(_):
    session.clear_all()
    print("Session cleared.")


def cmd_config(_):
    for k, v in CONFIG.summary().items():
        print(f"{k:12}: {v}")


def cmd_version(_):
    print(CONFIG.version)


def cmd_chat(args):
    if not args:
        print("Usage: chat <message>")
        return
    if not chat_available():
        print("Chat is disabled. AELM runs fully offline by default.\n"
              "To enable, set AELM_HF_TOKEN (and optionally AELM_API_URL\n"
              "to point at a local model server for a self-hosted setup).")
        return
    print("\nAELM\n" + "-" * 30)
    print(chat(" ".join(args)))
    print()


COMMANDS = {
    "load": cmd_load,
    "analyze": cmd_analyze,
    "dashboard": cmd_dashboard,
    "ats": cmd_ats,
    "rewrite": cmd_rewrite,
    "coverletter": cmd_coverletter,
    "interview": cmd_interview,
    "market": cmd_market,
    "risk": cmd_risk,
    "export": cmd_export,
    "status": cmd_status,
    "clear": cmd_clear,
    "config": cmd_config,
    "version": cmd_version,
    "chat": cmd_chat,
}


# ---------------------------------------------------------------- REPL

def run() -> int:
    print(BANNER)
    while True:
        try:
            raw = input("AELM> ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nGoodbye.")
            return 0

        if not raw:
            continue

        parts = raw.split()
        cmd, args = parts[0].lower(), parts[1:]

        if cmd in ("exit", "quit"):
            print("Goodbye.")
            return 0
        if cmd == "help":
            print(HELP_TEXT)
            continue

        handler = COMMANDS.get(cmd)
        if handler is None:
            print(f"Unknown command '{cmd}'. Type 'help'.")
            continue

        try:
            handler(args)
        except Exception as exc:
            print(f"Error: {exc}")


def main() -> None:
    sys.exit(run())
