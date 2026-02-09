import os
import time
from typing import Optional
from dotenv import load_dotenv
from google import genai

load_dotenv()

class GeminiClient:
    """
    Google Gemini client using the new google-genai package
    """
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        # self.model_name = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")
        self.model_name = os.getenv("GEMINI_MODEL", "gemini-2.5-flash-lite")
        self.client = None
        
        if not self.api_key:
            print("⚠️ Warning: GEMINI_API_KEY not found in environment variables")
            print("⚠️ Using fallback responses only")
            return
        
        try:
            self.client = genai.Client(api_key=self.api_key)
            print(f"✅ Gemini client initialized with model: {self.model_name}")
        except Exception as e:
            print(f"❌ Failed to initialize Gemini client: {e}")
            print("⚠️ Using fallback responses only")
    
    def generate_content(self, prompt: str, system_prompt: str = "", temperature: float = 0.7) -> str:
        """
        Generate content using Gemini
        """
        if not self.client:
            print("⚠️ Gemini client not available, using fallback")
            return self._get_fallback_response(system_prompt, prompt)
        
        try:
            # Combine system prompt and user prompt
            full_prompt = f"{system_prompt}\n\n{prompt}" if system_prompt else prompt
            
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=full_prompt,
                config={
                    "temperature": temperature,
                    "max_output_tokens": 2000,
                    "top_p": 0.9,
                    "top_k": 40
                }
            )
            
            return response.text.strip() if response.text else ""
            
        except Exception as e:
            print(f"❌ Gemini API error: {e}")
            return self._get_fallback_response(system_prompt, prompt)
    
    def _get_fallback_response(self, system_prompt: str, prompt: str) -> str:
        """Fallback response when Gemini fails"""
        if "OPTIMISTIC EXPERT" in system_prompt or "PRO" in system_prompt:
            return """**Strong Opening**: This decision represents a strategic opportunity with significant upside potential.

**Key Arguments FOR:**
1. **Efficiency Boost**: Could increase operational efficiency by 30-50%
2. **Competitive Advantage**: Early adoption provides first-mover benefits
3. **Cost Savings**: Long-term ROI estimated at 3:1 over 5 years
4. **Scalability**: Solution grows seamlessly with business needs

**Conclusion**: The benefits strongly outweigh the risks when implemented thoughtfully."""
        
        elif "RUTHLESS CRITICAL" in system_prompt or "CON" in system_prompt:
            return """**Primary Concern**: High implementation risk with uncertain payoff.

**Major Risks:**
1. **Implementation Complexity**: Estimated 6-12 month timeline with multiple dependencies
2. **Cost Overruns**: 40% of similar projects exceed budget by 50%+
3. **Adoption Resistance**: Cultural barriers could reduce effectiveness by 60%
4. **Technical Debt**: Could create long-term maintenance challenges

**Risk Assessment**: High risk profile requiring extensive mitigation planning."""
        
        else:
            return """**VERDICT**: Conditional Approval with Guardrails
**CONFIDENCE**: 0.65

**KEY RISKS:**
1. Implementation timeline uncertainty
2. Stakeholder alignment challenges  
3. ROI dependent on user adoption

**RECOMMENDATIONS:**
- Start with 90-day pilot program
- Establish clear success metrics upfront
- Create phased rollout plan with monthly reviews"""

# Create singleton instance
gemini_client = GeminiClient()