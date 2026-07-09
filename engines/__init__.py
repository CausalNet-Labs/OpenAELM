"""Local analysis engines. Every engine here runs offline."""

from .semantic_matcher import compare_resume_to_job, MatchResult
from .ats_engine import evaluate_ats, ATSResult
from .hire_probability import estimate_hire_probability, HireProbabilityResult
from .risk_intelligence import evaluate_job_risk, RiskResult
from .fraud_detection import evaluate_fraud, FraudResult
from .entry_barriers import evaluate_entry_barriers, EntryBarrierResult
from .market_opportunity import evaluate_market_opportunities, MarketOpportunityResult
from .cover_letter import generate_cover_letter, CoverLetterResult
from .interview_engine import generate_interview, InterviewResult
from .resume_rewriter import rewrite_resume, RewriteResult
from .dashboard import build_dashboard, DashboardResult

__all__ = [
    "compare_resume_to_job", "MatchResult",
    "evaluate_ats", "ATSResult",
    "estimate_hire_probability", "HireProbabilityResult",
    "evaluate_job_risk", "RiskResult",
    "evaluate_fraud", "FraudResult",
    "evaluate_entry_barriers", "EntryBarrierResult",
    "evaluate_market_opportunities", "MarketOpportunityResult",
    "generate_cover_letter", "CoverLetterResult",
    "generate_interview", "InterviewResult",
    "rewrite_resume", "RewriteResult",
    "build_dashboard", "DashboardResult",
]
