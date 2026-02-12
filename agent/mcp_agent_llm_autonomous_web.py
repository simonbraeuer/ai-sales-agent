from agent.ai_agent_llm_autonomous_web import AIOfferAgentAutonomousWeb

class MCPLLMAgentAutonomousWeb:
    """MCP-compatible wrapper for the AI agent."""
    def __init__(self, backend_url: str):
        self.agent = AIOfferAgentAutonomousWeb(backend_url)

    def run(self, session_id: str, user_input: str):
        """Run the agent with session context."""
        return self.agent.run_query(session_id, user_input)
