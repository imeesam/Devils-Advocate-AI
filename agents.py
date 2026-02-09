from groq_client import call_groq
from prompts import PRO_SYSTEM, CON_SYSTEM, JUDGE_SYSTEM

def pro_agent(question):
    return call_groq(PRO_SYSTEM, question)

def con_agent(question):
    return call_groq(CON_SYSTEM, question)

def judge_agent(pro_output, con_output, question):
    combined = f"""ORIGINAL QUESTION: {question}

ARGUMENTS FOR:
{pro_output}

ARGUMENTS AGAINST:
{con_output}

Please evaluate both sides and provide a structured verdict."""
    
    return call_groq(JUDGE_SYSTEM, combined)

# Optional reflection agent
def reflection_agent(verdict):
    reflection_prompt = """You are a meta-critic. Analyze this verdict for:
1. Hidden assumptions made
2. Potential blind spots
3. What additional information would be valuable
4. How the verdict could be improved
    
Be concise and critical."""
    
    return call_groq(reflection_prompt, verdict)