import random
from gemini_client import gemini_client
from prompts import PRO_SYSTEM, CON_SYSTEM, JUDGE_SYSTEM

def pro_agent(question):
    angle = random.choice([
        "Focus on short-term benefits.",
        "Focus on long-term strategic value.",
        "Assume a startup with limited budget.",
        "Assume an enterprise-scale organization."
    ])
    prompt = f"{angle}\n\nQUESTION: {question}"
    return gemini_client.generate_content(
        prompt,
        system_prompt=PRO_SYSTEM,
        temperature=0.9
    )

def con_agent(question):
    angle = random.choice([
        "Focus on financial risks.",
        "Focus on operational complexity.",
        "Focus on ethical and social risks.",
        "Focus on long-term maintainability."
    ])
    prompt = f"{angle}\n\nQUESTION: {question}"
    return gemini_client.generate_content(
        prompt,
        system_prompt=CON_SYSTEM,
        temperature=0.9
    )

def judge_agent(pro_output, con_output, question):
    combined = f"""
ORIGINAL QUESTION:
{question}

ARGUMENTS FOR:
{pro_output}

ARGUMENTS AGAINST:
{con_output}

Evaluate both sides and provide a verdict.
"""
    return gemini_client.generate_content(
        combined,
        system_prompt=JUDGE_SYSTEM,
        temperature=0.7
    )

def reflection_agent(verdict):
    reflection_prompt = """You are a meta-critic.
Analyze the verdict for:
1. Hidden assumptions
2. Blind spots
3. Missing information
4. How it could be improved

Be concise."""
    return gemini_client.generate_content(
        verdict,
        system_prompt=reflection_prompt,
        temperature=0.6
    )
