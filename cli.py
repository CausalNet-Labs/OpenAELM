"""
Integrated CLI for AELM
"""

from config import BANNER
from commands import (
    load_resume_command,
    load_job_command,
    analyze_command,
    dashboard_command,
    export_command,
    status_command,
)

def run():
    print(BANNER)
    print("Type 'help' for commands.\n")

    while True:
        try:
            raw = input("AELM> ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nGoodbye.")
            break

        if not raw:
            continue

        parts = raw.split()
        cmd = parts[0].lower()

        try:
            if cmd == "help":
                print("""Commands:
help
load resume <file>
load job <file>
analyze
dashboard
status
export txt|md|json
exit""")

            elif cmd == "load" and len(parts) >= 3:
                target = parts[1].lower()
                path = " ".join(parts[2:])
                if target == "resume":
                    load_resume_command(path)
                elif target == "job":
                    load_job_command(path)
                else:
                    print("Usage: load resume <file> | load job <file>")

            elif cmd == "analyze":
                analyze_command()

            elif cmd == "dashboard":
                dashboard_command()

            elif cmd == "status":
                status_command()

            elif cmd == "export" and len(parts) == 2:
                export_command(parts[1])

            elif cmd == "exit":
                break

            else:
                print("Unknown command. Type 'help'.")
        except Exception as e:
            print(f"Error: {e}")
