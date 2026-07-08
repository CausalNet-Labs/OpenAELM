"""
==============================================================================
pipeline.py
Advanced Employment & Labor Model (AELM)
Analysis Pipeline
==============================================================================
"""

from session import session

from resume_parser import parse_resume
from job_parser import parse_job
from semantic_matcher import compare_resume_to_job
from ats_engine import evaluate_ats
from hire_probability import estimate_hire_probability
from risk_intelligence import evaluate_job_risk
from fraud_detection import evaluate_fraud
from entry_barriers import evaluate_entry_barriers
from market_opportunity import evaluate_market_opportunities
from cover_letter import generate_cover_letter
from interview_engine import generate_interview
from dashboard import build_dashboard


class Pipeline:

    def validate(self):
        if not session.resume_text:
            raise RuntimeError("No resume loaded.")
        if not session.job_text:
            raise RuntimeError("No job description loaded.")

    def run(self):
        self.validate()

        print("[1/10] Parsing resume...")
        session.resume = parse_resume(session.resume_text)

        print("[2/10] Parsing job...")
        session.job = parse_job(session.job_text)

        print("[3/10] Semantic matching...")
        session.semantic = compare_resume_to_job(
            session.resume,
            session.job
        )

        print("[4/10] ATS analysis...")
        session.ats = evaluate_ats(
            session.resume,
            session.job,
            session.semantic
        )

        print("[5/10] Hire probability...")
        session.hire_probability = estimate_hire_probability(
            session.resume,
            session.job,
            session.semantic,
            session.ats
        )

        print("[6/10] Risk analysis...")
        session.risk = evaluate_job_risk(session.job)

        print("[7/10] Fraud analysis...")
        session.fraud = evaluate_fraud(session.job_text)

        print("[8/10] Entry barriers...")
        session.entry_barriers = evaluate_entry_barriers(session.job)

        print("[9/10] Market opportunities...")
        session.market = evaluate_market_opportunities(session.resume)

        print("[10/10] Finalizing...")
        session.cover_letter = generate_cover_letter(
            session.resume,
            session.job
        )

        session.interview = generate_interview(
            session.resume,
            session.job,
            session.semantic
        )

        session.dashboard = build_dashboard(
            session.ats,
            session.hire_probability,
            session.risk,
            session.fraud,
            session.entry_barriers
        )

        session.analyzed = True

        print("\nAnalysis complete.")
        return session.dashboard


def analyze():
    return Pipeline().run()


if __name__ == "__main__":
    analyze()
