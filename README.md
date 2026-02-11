# 😈 Devil’s Advocate Agent

A multi-agent decision system built with Google Gemini.

## What it does
Instead of producing a single answer, the system:
1. Generates a PRO argument
2. Generates a CON argument
3. Uses a JUDGE agent to weigh both
4. Produces a verdict with confidence and risks
    - *The confidence score reflects the Judge agent’s relative certainty based on argument strength, not a statistical probability.*
## Why it’s agentic
- Multiple specialized agents
- Structured deliberation
- Self-reflection step
- Explainable outputs

## Tech
- Google Gemini (gemini-2.5-flash-lite)
- Streamlit
- Python (3.10 recommended)

## Run locally
1. Add your Gemini API key to `.env`
2. `pip install -r requirements.txt`
3. `streamlit run app.py`
