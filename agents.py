from gemini_client import gemini_client
from prompts import PRO_SYSTEM, CON_SYSTEM, JUDGE_SYSTEM

def pro_agent(question):
    return gemini_client.generate_content(question, system_prompt=PRO_SYSTEM)

def con_agent(question):
    return gemini_client.generate_content(question, system_prompt=CON_SYSTEM)

def judge_agent(pro_output, con_output, question):
    combined = f"""ORIGINAL QUESTION: {question}

ARGUMENTS FOR:
{pro_output}

ARGUMENTS AGAINST:
{con_output}

Please evaluate both sides and provide a structured verdict."""
    
    return gemini_client.generate_content(combined, system_prompt=JUDGE_SYSTEM)

# Optional reflection agent
def reflection_agent(verdict):
    reflection_prompt = """You are a meta-critic. Analyze this verdict for:
1. Hidden assumptions made
2. Potential blind spots
3. What additional information would be valuable
4. How the verdict could be improved
    
Be concise and critical."""
    
    return gemini_client.generate_content(verdict, system_prompt=reflection_prompt)