"""
==============================================================================
export.py
Advanced Employment & Labor Model (AELM)
Export Utilities
==============================================================================
"""

import json
from datetime import datetime
from pathlib import Path


class ExportEngine:

    def __init__(self, output_dir="exports"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def _stamp(self):
        return datetime.now().strftime("%Y%m%d_%H%M%S")

    def export_txt(self, dashboard):
        path = self.output_dir / f"aelm_report_{self._stamp()}.txt"

        with open(path, "w", encoding="utf-8") as f:
            f.write("AELM Strategic Dashboard\n")
            f.write("=" * 40 + "\n\n")
            f.write(f"ATS Score: {dashboard.ats_survivability_score}\n")
            f.write(f"Hire Probability: {dashboard.hire_probability}\n")
            f.write(f"Fraud Verdict: {dashboard.fraud_verdict}\n\n")

            f.write("Top Resume Fixes\n")
            for item in dashboard.top_resume_fixes:
                f.write(f"- {item}\n")

            f.write("\nJob Risk Flags\n")
            for item in dashboard.job_risk_flags:
                f.write(f"- {item}\n")

            f.write("\nEntry Barriers\n")
            for item in dashboard.entry_barriers:
                f.write(f"- {item}\n")

            f.write("\nRecommended Next Action\n")
            f.write(dashboard.recommended_next_action + "\n")

        return str(path)

    def export_md(self, dashboard):
        path = self.output_dir / f"aelm_report_{self._stamp()}.md"

        with open(path, "w", encoding="utf-8") as f:
            f.write("# AELM Strategic Dashboard\n\n")
            f.write(f"**ATS Score:** {dashboard.ats_survivability_score}\n\n")
            f.write(f"**Hire Probability:** {dashboard.hire_probability}\n\n")
            f.write("## Resume Fixes\n")
            for item in dashboard.top_resume_fixes:
                f.write(f"- {item}\n")

            f.write("\n## Job Risks\n")
            for item in dashboard.job_risk_flags:
                f.write(f"- {item}\n")

            f.write("\n## Fraud Verdict\n")
            f.write(f"{dashboard.fraud_verdict}\n")

            f.write("\n## Next Action\n")
            f.write(dashboard.recommended_next_action + "\n")

        return str(path)

    def export_json(self, dashboard):
        path = self.output_dir / f"aelm_report_{self._stamp()}.json"

        with open(path, "w", encoding="utf-8") as f:
            json.dump(dashboard.__dict__, f, indent=2)

        return str(path)


if __name__ == "__main__":
    print("Export Engine Ready")
