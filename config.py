"""Central configuration for AELM.

Everything runs locally by default. The optional LLM chat feature reads
its settings from environment variables so no secrets live in code.
"""

import os
from dataclasses import dataclass, field
from typing import Dict


@dataclass(frozen=True)
class Config:
    app_name: str = "AELM"
    version: str = "2.0.0"

    # --- Optional LLM chat (disabled unless a token is provided) ---
    api_url: str = os.environ.get(
        "AELM_API_URL", "https://router.huggingface.co/v1/chat/completions"
    )
    model: str = os.environ.get("AELM_MODEL", "Qwen/Qwen3-235B-A22B-Instruct-2507")
    api_token: str = os.environ.get("AELM_HF_TOKEN", "")
    temperature: float = float(os.environ.get("AELM_TEMPERATURE", "0.4"))
    max_tokens: int = int(os.environ.get("AELM_MAX_TOKENS", "2000"))
    timeout: int = int(os.environ.get("AELM_TIMEOUT", "120"))
    max_history: int = int(os.environ.get("AELM_MAX_HISTORY", "40"))

    # --- Local engine settings ---
    export_dir: str = os.environ.get("AELM_EXPORT_DIR", "exports")
    max_score: int = 100

    def summary(self) -> Dict[str, str]:
        return {
            "Application": self.app_name,
            "Version": self.version,
            "Mode": "Local (decentralized)" + (
                " + optional LLM chat" if self.api_token else ""
            ),
            "LLM chat": "enabled" if self.api_token else
                        "disabled (set AELM_HF_TOKEN to enable)",
            "Model": self.model if self.api_token else "-",
            "Export dir": self.export_dir,
        }


CONFIG = Config()

BANNER = f"""
===========================================================
 {CONFIG.app_name} v{CONFIG.version}
 Advanced Employment & Labor Model
 Local-first · No account · No required network access
 Type 'help' for commands.
===========================================================
"""
