import os
import json
import re

def should_use_llm() -> bool:
    """
    Decide whether to use OpenAI LLM logic based on AI_SALES_AGENT_MODE.

    Modes:
        - auto: use LLM when OPENAI_API_KEY is set (default)
        - real: require OPENAI_API_KEY and always use LLM
        - fake: always use rule-based logic

    Returns:
        bool: True when the LLM should be used, False for rule-based logic.

    Raises:
        ValueError: If AI_SALES_AGENT_MODE is not one of auto, fake, or real.
        RuntimeError: If AI_SALES_AGENT_MODE is real without OPENAI_API_KEY set.
    """
    mode = os.getenv("AI_SALES_AGENT_MODE", "auto").lower()
    if mode not in {"auto", "fake", "real"}:
        raise ValueError(f"Unknown AI_SALES_AGENT_MODE '{mode}'. Use auto, fake, or real.")
    api_key = os.getenv("OPENAI_API_KEY")
    if mode == "fake":
        return False
    if mode == "real":
        if not api_key:
            raise RuntimeError(
                "OPENAI_API_KEY environment variable is required when AI_SALES_AGENT_MODE='real'"
            )
        return True
    return bool(api_key)

def parse_query_to_criteria_advanced(query: str) -> dict:
    """
    Parse user query into structured criteria for the offers API.
    This is a simple rule-based parser that extracts key information.
    In production, you would use an LLM for better parsing.
    """
    criteria = {}
    query_lower = query.lower()
    
    # Parse category
    if "fashion" in query_lower or "clothes" in query_lower or "shirt" in query_lower or "shoes" in query_lower:
        criteria["category"] = "fashion"
    elif "electronics" in query_lower or "laptop" in query_lower or "phone" in query_lower or "smartphone" in query_lower:
        criteria["category"] = "electronics"
    
    # Parse price constraints
    price_match = re.search(r'under\s+\$?(\d+)', query_lower)
    if price_match:
        criteria["max_price"] = float(price_match.group(1))
    
    price_match2 = re.search(r'below\s+\$?(\d+)', query_lower)
    if price_match2:
        criteria["max_price"] = float(price_match2.group(1))
    
    # Parse discount constraints
    discount_match = re.search(r'discount\s+above\s+(\d+)', query_lower)
    if discount_match:
        criteria["min_discount"] = float(discount_match.group(1))
    
    discount_match2 = re.search(r'(\d+)%\s+off', query_lower)
    if discount_match2:
        criteria["min_discount"] = float(discount_match2.group(1))
    
    # Parse rating constraints
    rating_match = re.search(r'rating\s+above\s+([\d.]+)', query_lower)
    if rating_match:
        criteria["min_rating"] = float(rating_match.group(1))
    
    return criteria


def parse_query_to_criteria_with_llm(query: str) -> dict:
    """
    Parse user query using OpenAI LLM for better understanding.
    Falls back to rule-based parsing if API key is not available,
    unless AI_SALES_AGENT_MODE=real forces LLM usage.
    """
    if not should_use_llm():
        # Fallback to rule-based parsing
        return parse_query_to_criteria_advanced(query)
    
    try:
        import openai
        openai.api_key = os.getenv("OPENAI_API_KEY")
        
        prompt = f"""
Parse the following user query into structured search criteria for an e-commerce offers API.
Extract: category (fashion or electronics), max_price, min_discount, min_rating.
Only include fields that are mentioned or implied in the query.

User query: "{query}"

Respond ONLY with a valid JSON object containing the criteria. Example: {{"category": "fashion", "max_price": 50}}
"""
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )
        
        content = response.choices[0].message.content.strip()
        # Extract JSON from response
        json_match = re.search(r'\{.*\}', content, re.DOTALL)
        if json_match:
            return json.loads(json_match.group())
        else:
            return json.loads(content)
    except Exception as e:
        print(f"LLM parsing failed: {e}, falling back to rule-based parsing")
        return parse_query_to_criteria_advanced(query)
