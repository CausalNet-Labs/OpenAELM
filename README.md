# AELM --- Advanced Employment & Labor Model

## Overview

AELM is a modular Python application that analyzes resumes and job
descriptions, estimates ATS compatibility, generates truthful resume
rewrites, evaluates job risks, detects common scam indicators, prepares
interview questions, and produces a strategic dashboard.

## Features

-   Resume parsing
-   Job description parsing
-   Semantic resume/job matching
-   ATS scoring
-   Resume rewriting
-   Hire probability estimation (heuristic)
-   Job risk intelligence
-   Fraud detection
-   Entry barrier analysis
-   Market opportunity recommendations
-   Cover letter generation
-   Interview preparation
-   Strategic dashboard
-   Export to TXT, Markdown, and JSON

## Installation

``` bash
pip install -r requirements.txt
```

## Run

``` bash
python aelm.py
```

Enter your Hugging Face API token when prompted.

## Project Structure

-   config.py
-   system_prompt.py
-   aelm.py
-   resume_parser.py
-   job_parser.py
-   semantic_matcher.py
-   ats_engine.py
-   resume_rewriter.py
-   hire_probability.py
-   risk_intelligence.py
-   fraud_detection.py
-   entry_barriers.py
-   market_opportunity.py
-   cover_letter.py
-   interview_engine.py
-   dashboard.py
-   export.py

## Commands

-   help
-   clear
-   config
-   version
-   resume
-   job
-   analyze
-   rewrite
-   ats
-   coverletter
-   interview
-   dashboard
-   export
-   exit

## Design Principles

-   Never fabricate qualifications.
-   Use heuristic estimates where appropriate.
-   Keep resume optimizations truthful.
-   Ask for missing information rather than guessing.


## Local Mode
This package has been modified to remove the Hugging Face router requirement. It starts directly into the local CLI.
