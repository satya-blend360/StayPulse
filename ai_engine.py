import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

class StayPulseAIEngine:
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in .env")
        self.client = OpenAI(api_key=api_key)

    def get_executive_insights(self, brand_name, kpis, problem_impact, sample_comments):
        """
        Generates a 2-sentence CEO Summary and a 3-point Action Plan.
        """
        prompt = f"""
        You are a senior Hospitality Consultant for Wyndham Hotels. 
        Analyze this data for the brand '{brand_name}':
        - NPS: {kpis['nps']}
        - OSAT: {kpis['osat']}
        - Responses: {kpis['responses']}
        - Problem Rate: {problem_impact['rate']}%
        - Problem-Free NPS: {problem_impact['nps_without_problem']}
        - With-Problem NPS: {problem_impact['nps_with_problem']}
        
        Sample Comments (Guest Voice):
        {chr(10).join(sample_comments[:10])}

        Generate a JSON response with exactly two keys:
        1. 'ceo_summary': A sharp, 2-sentence summary of the brand health.
        2. 'action_plan': A list of 3 specific, data-driven 'Fix-It' steps.
        
        Keep the tone professional, direct, and executive. Return only JSON.
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"}
            )
            import json
            return json.loads(response.choices[0].message.content)
        except Exception as e:
            print(f"AI Error: {e}")
            return {
                "ceo_summary": "Data-driven summary unavailable at this moment.",
                "action_plan": ["Review operational standards.", "Monitor guest feedback.", "Investigate problem hotspots."]
            }
