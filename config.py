"""
==============================================================================
AELM CONFIGURATION
==============================================================================

Global configuration for the Advanced Employment & Labor Model.
"""

APP_NAME = "AELM"
VERSION = "1.0.0"

API_URL = "https://router.huggingface.co/v1/chat/completions"

MODEL = "Qwen/Qwen3-235B-A22B-Instruct-2507"

TEMPERATURE = 0.4
MAX_TOKENS = 2000
TIMEOUT = 120
MAX_HISTORY = 40

ALLOW_RESUME_REWRITE = True
ALLOW_COVER_LETTERS = True
ALLOW_INTERVIEW_MODE = True
ALLOW_EXPORT = True

ATS_KEYWORD_WEIGHT = 0.35
ATS_FORMAT_WEIGHT = 0.20
ATS_EXPERIENCE_WEIGHT = 0.25
ATS_SKILL_WEIGHT = 0.20

ENABLE_HIRE_PROBABILITY = True
ENABLE_JOB_RISK = True
ENABLE_FRAUD_SCAN = True
ENABLE_ENTRY_BARRIERS = True
ENABLE_AUTOMATION_SCORE = True

EXPORT_MD = True
EXPORT_TXT = True
EXPORT_JSON = True
EXPORT_PDF = False

MAX_SCORE = 100

COMMANDS = {
    "help":"Show help menu",
    "clear":"Clear conversation",
    "resume":"Load or analyze resume",
    "job":"Load job description",
    "analyze":"Run full pipeline",
    "rewrite":"Generate ATS resume",
    "ats":"ATS analysis",
    "coverletter":"Generate cover letter",
    "interview":"Interview preparation",
    "dashboard":"Strategic dashboard",
    "export":"Export results",
    "config":"Show configuration",
    "version":"Show version",
    "exit":"Exit program"
}

BANNER = f"""
===========================================================
 {APP_NAME} v{VERSION}

 Advanced Employment & Labor Model

 Type 'help' for commands.
===========================================================
"""
