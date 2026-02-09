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
    return gemini_client.generate_content(prompt, system_prompt=PRO_SYSTEM, temperature=0.9)

def con_agent(question):
    angle = random.choice([
        "Focus on financial risks.",
        "Focus on operational complexity.",
        "Focus on ethical and social risks.",
        "Focus on long-term maintainability."
    ])
    prompt = f"{angle}\n\nQUESTION: {question}"
    return gemini_client.generate_content(prompt, system_prompt=CON_SYSTEM, temperature=0.9)
