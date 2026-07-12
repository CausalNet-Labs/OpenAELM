"""Terminal presentation layer.

Uses `rich` for colors, tables, panels, and progress bars when it is
installed. Falls back to plain text automatically, so AELM keeps its
zero-required-dependency promise.
"""

import re

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table
    from rich.rule import Rule
    from rich.progress import (
        Progress, SpinnerColumn, BarColumn, TextColumn,
        TimeElapsedColumn,
    )
    HAS_RICH = True
    console = Console(highlight=False)
except ImportError:  # plain-text mode
    HAS_RICH = False
    console = None

_NUM = re.compile(r"-?\d+")

ACCENT = "cyan"


def _score_color(value) -> str:
    """green/yellow/red based on the first number found in the value."""
    m = _NUM.search(str(value))
    if not m:
        return "white"
    n = int(m.group())
    if n >= 75:
        return "green"
    if n >= 50:
        return "yellow"
    return "red"


def _risk_color(value) -> str:
    v = str(value).lower()
    if any(w in v for w in ("high", "severe", "critical", "scam", "avoid")):
        return "red"
    if any(w in v for w in ("medium", "moderate", "caution", "possible")):
        return "yellow"
    if any(w in v for w in ("low", "clean", "safe", "legitimate", "pass")):
        return "green"
    return "white"


# ------------------------------------------------------------------ basics

def banner(app_name: str, version: str) -> None:
    if HAS_RICH:
        console.print(Panel(
            f"[bold {ACCENT}]{app_name}[/bold {ACCENT}] "
            f"[dim]v{version}[/dim]\n"
            "Advanced Employment & Labor Model\n"
            "[dim]Local-first · No account · No required network access[/dim]\n"
            f"Type [bold]help[/bold] for commands.",
            border_style=ACCENT, expand=False, padding=(0, 4)))
    else:
        print("=" * 59)
        print(f" {app_name} v{version}")
        print(" Advanced Employment & Labor Model")
        print(" Local-first · No account · No required network access")
        print(" Type 'help' for commands.")
        print("=" * 59)


def info(msg: str) -> None:
    if HAS_RICH:
        console.print(msg)
    else:
        print(msg)


def success(msg: str) -> None:
    if HAS_RICH:
        console.print(f"[green]✓[/green] {msg}")
    else:
        print(msg)


def error(msg: str) -> None:
    if HAS_RICH:
        console.print(f"[bold red]Error:[/bold red] {msg}")
    else:
        print(f"Error: {msg}")


def hint(msg: str) -> None:
    if HAS_RICH:
        console.print(f"[dim]{msg}[/dim]")
    else:
        print(msg)


def rule(title: str = "") -> None:
    if HAS_RICH:
        console.print(Rule(title, style=ACCENT))
    else:
        line = "=" * 60
        print(f"\n{line}\n{title}\n{line}" if title else line)


# ------------------------------------------------------------------ blocks

def kv_table(rows, title: str = None, color: str = "score") -> None:
    """rows: list of (label, value). color: 'score' | 'risk' | None."""
    pick = {"score": _score_color, "risk": _risk_color}.get(color)
    if HAS_RICH:
        t = Table(show_header=False, box=None, padding=(0, 2, 0, 0))
        t.add_column(style="bold")
        t.add_column()
        for label, value in rows:
            style = pick(value) if pick else "white"
            t.add_row(label, f"[{style}]{value}[/{style}]")
        if title:
            console.print(f"\n[bold]{title}[/bold]")
        console.print(t)
    else:
        if title:
            print(f"\n{title}")
        width = max(len(l) for l, _ in rows) if rows else 0
        for label, value in rows:
            print(f"{label:<{width}} : {value}")


def bullets(title: str, items, style: str = ACCENT,
            empty: str = None) -> None:
    if not items and empty is None:
        return
    shown = items or [empty]
    if HAS_RICH:
        console.print(f"\n[bold {style}]{title}[/bold {style}]")
        for item in shown:
            console.print(f"  [dim]•[/dim] {item}")
    else:
        print(f"\n{title}:")
        for item in shown:
            print(f"  - {item}")


def panel(text: str, title: str = None) -> None:
    if HAS_RICH:
        console.print(Panel(text, title=title, border_style=ACCENT,
                            padding=(1, 2)))
    else:
        if title:
            print(f"\n--- {title} ---\n")
        print(text)


# ------------------------------------------------------------------ pipeline

def run_pipeline(analyze_fn) -> None:
    """Run the analysis pipeline with a live progress bar (rich only)."""
    if not HAS_RICH:
        analyze_fn(print)
        return

    done_note = []

    with Progress(
        SpinnerColumn(style=ACCENT),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(complete_style=ACCENT),
        TextColumn("{task.completed}/{task.total}"),
        TimeElapsedColumn(),
        console=console,
        transient=True,
    ) as progress:
        task = progress.add_task("Starting...", total=13)

        def report(msg: str) -> None:
            m = re.match(r"\[(\d+)/(\d+)\]\s*(.+)", msg.strip())
            if m:
                step, total, label = m.groups()
                progress.update(task, completed=int(step) - 1,
                                total=int(total),
                                description=label.rstrip("."))
            else:
                done_note.append(msg.strip())

        analyze_fn(report)
        progress.update(task, completed=progress.tasks[0].total,
                        description="Done")

    success("Analysis complete.")
    for note in done_note:
        text = note.replace("Analysis complete.", "").strip()
        if text:
            hint(text)
