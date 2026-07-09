"""Export the strategic dashboard to TXT, Markdown, or JSON."""

import json
from dataclasses import asdict, is_dataclass
from datetime import datetime
from pathlib import Path

from .config import CONFIG


class ExportEngine:
    def __init__(self, output_dir: str = None):
        self.output_dir = Path(output_dir or CONFIG.export_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def _path(self, ext: str) -> Path:
        stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return self.output_dir / f"aelm_report_{stamp}.{ext}"

    def export(self, fmt: str, dashboard) -> str:
        fmt = fmt.lower()
        if fmt == "txt":
            return self._txt(dashboard)
        if fmt == "md":
            return self._md(dashboard)
        if fmt == "json":
            return self._json(dashboard)
        raise ValueError("Supported formats: txt, md, json")

    def _txt(self, d) -> str:
        path = self._path("txt")
        lines = [
            "AELM Strategic Dashboard",
            "=" * 40, "",
            f"ATS Score: {d.ats_survivability_score}",
            f"Hire Probability: {d.hire_probability}",
            f"Fraud Verdict: {d.fraud_verdict}", "",
            "Top Resume Fixes",
            *[f"- {x}" for x in d.top_resume_fixes], "",
            "Job Risk Flags",
            *[f"- {x}" for x in d.job_risk_flags], "",
            "Entry Barriers",
            *[f"- {x}" for x in d.entry_barriers], "",
            "Recommended Next Action",
            d.recommended_next_action,
        ]
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        return str(path)

    def _md(self, d) -> str:
        path = self._path("md")
        lines = [
            "# AELM Strategic Dashboard", "",
            f"**ATS Score:** {d.ats_survivability_score}", "",
            f"**Hire Probability:** {d.hire_probability}", "",
            "## Resume Fixes",
            *[f"- {x}" for x in d.top_resume_fixes], "",
            "## Job Risks",
            *[f"- {x}" for x in d.job_risk_flags], "",
            "## Entry Barriers",
            *[f"- {x}" for x in d.entry_barriers], "",
            "## Fraud Verdict",
            d.fraud_verdict, "",
            "## Next Action",
            d.recommended_next_action,
        ]
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        return str(path)

    def _json(self, d) -> str:
        path = self._path("json")
        data = asdict(d) if is_dataclass(d) else d.__dict__
        path.write_text(json.dumps(data, indent=2), encoding="utf-8")
        return str(path)
