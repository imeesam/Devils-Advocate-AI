import os
import requests
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def call_groq(system_prompt, user_prompt):
    """
    Call Groq API directly using HTTP
    """
    if not GROQ_API_KEY:
        return get_mock_response(system_prompt, user_prompt)
    
    url = "https://api.groq.com/openai/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "llama-3.3-70b-versatile",  # Latest and best
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 1000,
        "top_p": 0.9,
        "stream": False
    }
    
    try:
        response = requests.post(url, headers=headers, json=data, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            return result['choices'][0]['message']['content']
        else:
            print(f"Groq API Error: {response.status_code}")
            return get_mock_response(system_prompt, user_prompt)
            
    except Exception as e:
        print(f"Groq connection error: {e}")
        return get_mock_response(system_prompt, user_prompt)

def get_mock_response(system_prompt, user_prompt):
    """
    Mock responses for when API fails (demo never crashes)
    """
    if "PRO" in system_prompt:
        return """**Arguments FOR:**
• **Efficiency**: Automates decision-making, reducing time by 40-60%
• **Accuracy**: Reduces human error and bias in complex analysis
• **Scalability**: Handles increasing volume without additional costs
• **Consistency**: Provides uniform evaluations across all cases"""
    
    elif "CON" in system_prompt:
        return """**Arguments AGAINST:**
• **Implementation Costs**: High initial setup ($50k-$200k) and ongoing maintenance
• **Over-reliance Risk**: May reduce critical human oversight and judgment
• **Bias Amplification**: Could perpetuate or amplify existing biases
• **Change Resistance**: Stakeholder pushback and adoption challenges"""
    
    else:  # Judge
        return """**FINAL VERDICT**: Conditional Approval
**CONFIDENCE SCORE**: 0.72 / 1.00
**KEY RISKS IDENTIFIED**:
1. Integration complexity with existing systems
2. Data privacy and security compliance
3. User training and adoption resistance
**RECOMMENDATIONS**:
• Start with a 3-month pilot program
• Implement continuous bias monitoring
• Maintain human-in-the-loop oversight
• Regular stakeholder feedback sessions"""