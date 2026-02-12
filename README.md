# AI Sales Agent - Interactive Web Demo

An AI-powered chatbot sales agent with a fully interactive web interface. The agent uses autonomous reasoning to understand user queries, interact with a REST backend, ask follow-up questions, and return personalized offers with explanations.

## Features

✨ **Multi-Turn Conversations**: Agent can ask clarifying questions and refine search criteria iteratively  
🤖 **Autonomous AI Agent**: Uses LLM (optional) or rule-based parsing to understand user intent  
🔍 **Dynamic Filtering**: Filter offers by category, price, discount, and rating  
📊 **Interactive Table View**: Sort offers by any column with a single click  
🎨 **Modern UI**: Beautiful gradient design with smooth animations  
💬 **Real-Time Chat**: Type queries naturally and get instant responses  

## Project Structure

```
ai-sales-agent/
├── backend.py                          # REST API with offers data
├── agent/                              # AI agent modules
│   ├── __init__.py
│   ├── llm_parser_advanced.py         # Query parsing (LLM or rule-based)
│   ├── ai_agent_llm_autonomous_web.py # Core autonomous agent logic
│   └── mcp_agent_llm_autonomous_web.py # MCP-compatible wrapper
├── web_app.py                          # FastAPI web interface
├── templates/
│   └── index.html                      # Chat UI template
├── static/
│   └── main.js                         # Frontend JavaScript
└── requirements.txt                    # Python dependencies
```

## Installation

1. **Clone the repository**:
```bash
git clone https://github.com/simonbraeuer/ai-sales-agent.git
cd ai-sales-agent
```

2. **Create a virtual environment**:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

4. **(Optional) Set up OpenAI API** for enhanced LLM-based parsing:
```bash
export OPENAI_API_KEY="your-api-key-here"  # On Windows: set OPENAI_API_KEY=your-api-key-here
```
*Note: The agent works without an API key using rule-based parsing.*

## Usage

### Start the Backend API

In one terminal, start the REST backend on port 8001:

```bash
uvicorn backend:app --reload --port 8001
```

The API will be available at `http://localhost:8001/offers`

### Start the Web Application

In another terminal, start the web interface on port 8000:

```bash
uvicorn web_app:app --reload --port 8000
```

### Open in Browser

Navigate to `http://localhost:8000` and start chatting!

## Example Queries

Try these sample queries:

- `"Find fashion items under $50"`
- `"Show electronics with discount above 10%"`
- `"I want items with rating above 4"`
- `"Looking for smartphones on sale"`
- `"Show me the best deals"`

## How It Works

1. **User Input**: User types a natural language query in the chat interface
2. **Query Parsing**: Agent parses the query into structured criteria (category, price, discount, rating)
3. **Backend Query**: Agent calls the REST API with the parsed criteria
4. **Decision Making**: Agent decides if results are satisfactory or if follow-up questions are needed
5. **Response**: Agent returns offers in a sortable table or asks clarifying questions
6. **Refinement**: User can answer follow-up questions to refine results
7. **Dynamic Sorting**: User can sort offers by any column (price, discount, rating, title)

## API Endpoints

### Backend API (Port 8001)

- `GET /offers`: Fetch offers with optional filters
  - Query parameters: `category`, `max_price`, `min_discount`, `min_rating`

### Web API (Port 8000)

- `GET /`: Main chat interface
- `POST /api/query`: Send query to AI agent
  - Request: `{"query": "user message", "session_token": "session-id"}`
  - Response: `{"message": "agent response", "offers": [...], "done": true/false}`

## Architecture

The agent uses a **stateful, session-based architecture**:

- Each browser session gets a unique token
- Conversation state is maintained across multiple turns
- Agent can refine criteria based on user feedback
- MCP (Model Context Protocol) compatible design

## Customization

### Adding More Offers

Edit `backend.py` and add items to the `OFFERS` list:

```python
OFFERS = [
    {"id": 5, "title": "New Product", "category": "electronics", 
     "price": 500, "discount": 20, "rating": 4.8},
    # Add more...
]
```

### Modifying UI Styles

Edit `templates/index.html` to customize colors, fonts, and layout.

### Extending Agent Logic

Edit `agent/ai_agent_llm_autonomous_web.py` to add more decision-making logic or criteria.

## Technologies Used

- **FastAPI**: Modern web framework for Python
- **Jinja2**: Template engine for HTML
- **Vanilla JavaScript**: No frontend framework dependencies
- **OpenAI API**: Optional LLM integration for better parsing
- **Uvicorn**: ASGI server for running the applications

## License

MIT License - feel free to use and modify for your projects!

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
