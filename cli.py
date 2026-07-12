"""AELM interactive terminal interface.

One CLI, one entry point. All commands work fully offline except
'chat', which is optional and clearly marked. Output is styled with
`rich` when installed and falls back to plain text otherwise.
"""

import sys

from .config import CONFIG
from .session import session
from .parsing import load_file
from .pipeline import analyze
from .engines import rewrite_resume
from .export import ExportEngine
from .llm import chat, chat_available
from . import ui

HELP_ROWS = [
    ("load resume <file>", "Load a resume (.txt .md .pdf .docx)"),
    ("load job <file>", "Load a job description"),
    ("analyze", "Run the full local analysis pipeline"),
    ("dashboard", "Strategic dashboard summary"),
    ("ats", "ATS survivability details"),
    ("rewrite [mode]", "Truthful resume rewrite (ats|minimal|plain)"),
    ("coverletter", "Generated cover letter"),
    ("interview", "Interview preparation questions"),
    ("market", "Adjacent role recommendations"),
    ("risk", "Job risk + fraud details"),
    ("export <txt|md|json>", "Export the dashboard to a file"),
    ("status", "Show session state"),
    ("clear", "Clear session (results + chat memory)"),
    ("config", "Show configuration"),
    ("version", "Show version"),
    ("chat <message>", "Optional LLM chat (requires AELM_HF_TOKEN)"),
    ("help", "Show this menu"),
    ("exit", "Quit"),
]


def _require_analysis() -> bool:
    if not session.analyzed:
        ui.hint("Run 'analyze' first (after loading a resume and a job).")
        return False
    return True


# ---------------------------------------------------------------- commands

def cmd_load(args):
    if len(args) < 2 or args[0].lower() not in ("resume", "job"):
        ui.hint("Usage: load resume <file>  |  load job <file>")
        return
    target, path = args[0].lower(), " ".join(args[1:])
    text = load_file(path)
    if target == "resume":
        session.resume_text, session.resume_path = text, path
    else:
        session.job_text, session.job_path = text, path
    session.clear_results()
    ui.success(f"Loaded {target}: {path} ({len(text)} chars)")


def cmd_analyze(_):
    ui.run_pipeline(analyze)


def cmd_dashboard(_):
    if not _require_analysis():
        return
    d = session.dashboard
    ui.rule("AELM STRATEGIC DASHBOARD")
    ui.kv_table([
        ("ATS Score", d.ats_survivability_score),
        ("Hire Probability", d.hire_probability),
        ("Fraud Verdict", d.fraud_verdict),
    ])
    ui.bullets("Top Resume Fixes", d.top_resume_fixes, empty="(none)")
    ui.bullets("Job Risk Flags", d.job_risk_flags, style="yellow",
               empty="(none)")
    ui.bullets("Entry Barriers", d.entry_barriers, empty="(none)")
    ui.bullets("Recommended Next Action", [d.recommended_next_action],
               style="green")
    ui.rule()


def cmd_ats(_):
    if not _require_analysis():
        return
    a = session.ats
    ui.rule("ATS ANALYSIS")
    ui.kv_table([
        ("ATS Survivability", f"{a.survivability_score}/100"),
        ("Keyword Coverage", f"{a.keyword_coverage}%"),
        ("Formatting Score", f"{a.formatting_score}/100"),
        ("Verdict", a.verdict),
    ])
    ui.bullets("Strengths", a.strengths, style="green")
    ui.bullets("Improvements", a.improvements, style="yellow")
    ui.info("")


def cmd_rewrite(args):
    if not _require_analysis():
        return
    mode = args[0].lower() if args else "ats"
    result = rewrite_resume(session.resume, session.job, mode)
    session.rewrite = result
    ui.panel(result.resume_text, title=f"Rewritten Resume ({result.mode})")
    ui.bullets("Notes", result.notes)
    ui.info("")


def cmd_coverletter(_):
    if not _require_analysis():
        return
    c = session.cover_letter
    ui.panel(c.cover_letter, title="Cover Letter")
    ui.bullets("Notes", c.notes)
    ui.info("")


def cmd_interview(_):
    if not _require_analysis():
        return
    iv = session.interview
    ui.rule("INTERVIEW PREP")
    for group, items in (
        ("Screening Questions", iv.screening),
        ("Behavioral Questions", iv.behavioral),
        ("Technical Questions", iv.technical),
    ):
        if items:
            ui.bullets(group, [f"{q.question}  ({q.reason})" for q in items])
    ui.bullets("Weak Points to Prepare", iv.weak_points, style="yellow")
    ui.bullets("Coaching", iv.coaching, style="green")
    ui.info("")


def cmd_market(_):
    if not _require_analysis():
        return
    m = session.market
    if m.opportunities:
        ui.bullets("Adjacent Role Opportunities", [
            f"{o.title} [{o.estimated_fit} fit] — {o.reason}"
            for o in m.opportunities
        ])
    for n in m.notes:
        ui.hint(f"({n})")
    ui.info("")


def cmd_risk(_):
    if not _require_analysis():
        return
    r, f = session.risk, session.fraud
    ui.rule("RISK & FRAUD")
    ui.kv_table([
        ("Burnout Risk", r.burnout_risk),
        ("Ghost Job Risk", r.ghost_job_risk),
        ("Layoff Risk", r.layoff_risk),
        ("Automation Risk", r.automation_risk),
    ], color="risk")
    ui.bullets("Risk Flags", r.flags, style="yellow")
    ui.kv_table([("Fraud Verdict", f"{f.verdict} (score {f.risk_score})")],
                color="risk")
    ui.bullets("Fraud Flags", f.flags, style="red")
    if f.warning:
        ui.error(f.warning)
    ui.bullets("Verification Steps", f.verification_steps, style="green")
    ui.info("")


def cmd_export(args):
    if not _require_analysis():
        return
    if len(args) != 1:
        ui.hint("Usage: export <txt|md|json>")
        return
    path = ExportEngine().export(args[0], session.dashboard)
    ui.success(f"Exported: {path}")


def cmd_status(_):
    for line in session.status_lines():
        ui.info(line)


def cmd_clear(_):
    session.clear_all()
    ui.success("Session cleared.")


def cmd_config(_):
    ui.kv_table(list(CONFIG.summary().items()), title="Configuration",
                color=None)


def cmd_version(_):
    ui.info(CONFIG.version)


def cmd_chat(args):
    if not args:
        ui.hint("Usage: chat <message>")
        return
    if not chat_available():
        ui.hint("Chat is disabled. AELM runs fully offline by default.\n"
                "To enable, set AELM_HF_TOKEN (and optionally AELM_API_URL\n"
                "to point at a local model server for a self-hosted setup).")
        return
    ui.panel(chat(" ".join(args)), title="AELM")


def cmd_help(_):
    ui.rule("COMMANDS")
    ui.kv_table(HELP_ROWS, color=None)
    ui.info("")


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
    "help": cmd_help,
}


# ---------------------------------------------------------------- REPL

def _prompt() -> str:
    if ui.HAS_RICH:
        return ui.console.input(f"[bold {ui.ACCENT}]AELM>[/bold {ui.ACCENT}] ")
    return input("AELM> ")


def run() -> int:
    ui.banner(CONFIG.app_name, CONFIG.version)
    while True:
        try:
            raw = _prompt().strip()
        except (KeyboardInterrupt, EOFError):
            ui.info("\nGoodbye.")
            return 0

        if not raw:
            continue

        parts = raw.split()
        cmd, args = parts[0].lower(), parts[1:]

        if cmd in ("exit", "quit"):
            ui.info("Goodbye.")
            return 0

        handler = COMMANDS.get(cmd)
        if handler is None:
            ui.hint(f"Unknown command '{cmd}'. Type 'help'.")
            continue

        try:
            handler(args)
        except Exception as exc:
            ui.error(str(exc))


def main() -> None:
    sys.exit(run())
