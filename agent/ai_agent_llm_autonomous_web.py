import requests
import os
import json
import re
from agent.llm_parser_advanced import parse_query_to_criteria_with_llm, should_use_llm

class AIOfferAgentAutonomousWeb:
    def __init__(self, backend_url: str):
        self.backend_url = backend_url
        self.session_state = {}  # Store conversation state per user/session

    def fetch_offers(self, criteria: dict):
        """Fetch offers from REST backend based on criteria."""
        try:
            response = requests.get(f"{self.backend_url}/offers", params=criteria, timeout=5)
            return response.json() if response.status_code == 200 else []
        except Exception as e:
            print(f"Error fetching offers: {e}")
            return []

    def decide_next_action_with_llm(self, query: str, offers: list, criteria: dict):
        """
        Decide if follow-up question is needed using LLM.
        Returns:
        - next_action: "DONE" or "ASK"
        - question: string (if ASK)
        """
        api_key = os.getenv("OPENAI_API_KEY")
        
        if not should_use_llm(api_key):
            # Without LLM, decide based on simple rules
            if len(offers) == 0:
                return {"next_action": "ASK", "question": "No offers found. Would you like to adjust your criteria?"}
            elif len(offers) > 10:
                return {"next_action": "ASK", "question": "Found many offers. Would you like to narrow down by rating or discount?"}
            else:
                return {"next_action": "DONE"}
        
        try:
            import openai
            openai.api_key = api_key
            
            prompt = f"""
You are an AI shopping assistant.

User query: "{query}"
Current criteria: {criteria}
Number of offers found: {len(offers)}

Decide if you need to ask the user a follow-up question to refine results.
If results are satisfactory (1-10 offers), respond with "DONE".
If no offers or too many offers, ask a clarifying question.

Respond ONLY as JSON: {{"next_action": "DONE" or "ASK", "question": "..." if ASK}}
"""
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0
            )
            
            content = response.choices[0].message.content.strip()
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            else:
                return json.loads(content)
        except Exception as e:
            print(f"LLM decision failed: {e}, using default")
            return {"next_action": "DONE"}

    def update_criteria_with_response(self, criteria: dict, user_response: str):
        """Update criteria based on user's answer (with or without LLM)."""
        api_key = os.getenv("OPENAI_API_KEY")
        
        if not should_use_llm(api_key):
            # Simple rule-based update
            user_lower = user_response.lower()
            if "yes" in user_lower or "higher" in user_lower:
                if "rating" in user_lower:
                    criteria["min_rating"] = criteria.get("min_rating", 0) + 0.5
                elif "discount" in user_lower:
                    criteria["min_discount"] = criteria.get("min_discount", 0) + 10
            return criteria
        
        try:
            import openai
            openai.api_key = api_key
            
            prompt = f"""
Current search criteria: {criteria}
User response: "{user_response}"

Update the criteria based on the user's response. Return ONLY a JSON object with the updated criteria.
Only include fields that need to be added or modified.

Example: {{"min_rating": 4.5, "max_price": 100}}
"""
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0
            )
            
            content = response.choices[0].message.content.strip()
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            if json_match:
                update = json.loads(json_match.group())
            else:
                update = json.loads(content)
            criteria.update(update)
        except Exception as e:
            print(f"LLM update failed: {e}, keeping criteria unchanged")
        
        return criteria

    def run_query(self, session_id: str, user_input: str):
        """
        Multi-turn query handler.
        session_id: unique for each user/browser session
        user_input: user query or follow-up response
        Returns dict with:
            - message: question or final reasoning
            - offers: list (if DONE)
            - done: bool
        """
        # Initialize session state if new
        if session_id not in self.session_state:
            self.session_state[session_id] = {
                "original_query": user_input,
                "criteria": parse_query_to_criteria_with_llm(user_input),
                "offers": [],
                "done": False
            }
            reasoning = f"Parsed initial criteria: {self.session_state[session_id]['criteria']}"
        else:
            # Update criteria with user follow-up response
            self.session_state[session_id]["criteria"] = self.update_criteria_with_response(
                self.session_state[session_id]["criteria"], user_input
            )
            reasoning = f"Updated criteria: {self.session_state[session_id]['criteria']}"

        criteria = self.session_state[session_id]["criteria"]
        offers = self.fetch_offers(criteria)
        self.session_state[session_id]["offers"] = offers

        decision = self.decide_next_action_with_llm(
            self.session_state[session_id]["original_query"],
            offers,
            criteria
        )

        if decision.get("next_action") == "DONE" or len(offers) == 0:
            # Sort offers by discount and rating
            offers.sort(key=lambda o: (-o.get("discount", 0), -o.get("rating", 0)))
            self.session_state[session_id]["done"] = True
            message = f"Found {len(offers)} offers matching your criteria.\n{reasoning}"
            return {"message": message, "offers": offers, "done": True}
        else:
            # Ask follow-up question
            question = decision.get("question", "Could you clarify your preferences?")
            return {"message": question, "offers": [], "done": False}
