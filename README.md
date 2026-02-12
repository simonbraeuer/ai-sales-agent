# AI Sales Agent - Interactive Web Demo

An AI-powered chatbot sales agent with a fully interactive web interface. The agent uses autonomous reasoning to understand user queries, filter offers, and return personalized recommendations with explanations.

## 🌐 Live Demo

**GitHub Pages:** [https://simonbraeuer.github.io/ai-sales-agent/](https://simonbraeuer.github.io/ai-sales-agent/)

The app runs entirely in your browser - no backend required!

## Features

✨ **Client-Side Only**: Runs entirely in the browser, perfect for GitHub Pages  
🤖 **Smart Query Parsing**: Understands natural language queries and extracts search criteria  
🔍 **Dynamic Filtering**: Filter offers by category, price, discount, and rating  
📊 **Interactive Table View**: Sort offers by any column with a single click  
🎨 **Modern UI**: Beautiful gradient design with smooth animations  
💬 **Real-Time Chat**: Type queries naturally and get instant responses  
⚡ **No Installation**: Just open `index.html` in a browser  

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

## 🚀 Quick Start (GitHub Pages Version)

The easiest way to use this app is via **GitHub Pages** - just visit the live demo!

Or run it locally:

1. Download `index.html` from this repository
2. Open it in any modern web browser
3. Start asking for offers!

No installation, no dependencies, no setup required!

## Example Queries

Try these sample queries in the chat interface:

- `"Find fashion items under $50"`
- `"Show electronics with discount above 20%"`
- `"I want items with rating above 4.5"`
- `"Looking for shoes"`
- `"Show me the best deals"`

## 📦 Python Backend Version (Advanced)

For development or if you want to extend the agent with OpenAI integration, you can run the full Python backend version:

### Installation

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

### Running the Backend Version

**Start the Backend API** (Terminal 1):
```bash
uvicorn backend:app --reload --port 8001
```

**Start the Web Application** (Terminal 2):
```bash
uvicorn web_app:app --reload --port 8000
```

**Open in Browser**: Navigate to `http://localhost:8000`

## 🎯 Project Structure

```
ai-sales-agent/
├── index.html                           # 🌐 Standalone GitHub Pages version
├── backend.py                           # REST API with offers data
├── agent/                               # AI agent modules
│   ├── __init__.py
│   ├── llm_parser_advanced.py          # Query parsing (LLM or rule-based)
│   ├── ai_agent_llm_autonomous_web.py  # Core autonomous agent logic
│   └── mcp_agent_llm_autonomous_web.py # MCP-compatible wrapper
├── web_app.py                           # FastAPI web interface
├── templates/
│   └── index.html                       # Chat UI template
├── static/
│   └── main.js                          # Frontend JavaScript
└── requirements.txt                     # Python dependencies
```

## 📖 How It Works

### GitHub Pages Version (Client-Side)
1. **User Input**: User types a natural language query
2. **Query Parsing**: JavaScript parses the query into structured criteria (category, price, discount, rating)
3. **Filtering**: Client-side filtering of the embedded offers data
4. **Display**: Results shown in a sortable, color-coded table
5. **Sorting**: Click any column header or use dropdowns to sort

### Python Backend Version
1. **User Input**: User types a natural language query in the chat interface
2. **Query Parsing**: Agent parses the query into structured criteria (LLM or rule-based)
3. **Backend Query**: Agent calls the REST API with the parsed criteria
4. **Decision Making**: Agent decides if results are satisfactory or if follow-up questions are needed
5. **Response**: Agent returns offers in a sortable table or asks clarifying questions
6. **Refinement**: User can answer follow-up questions to refine results
7. **Dynamic Sorting**: User can sort offers by any column (price, discount, rating, title)

## 🚢 Deploy to GitHub Pages

To deploy your own version:

1. **Fork this repository**
2. **Go to Settings** → **Pages**
3. **Select Source**: GitHub Actions
4. **Push to `main`** (or trigger the workflow manually)
5. Your site will be live at `https://<your-username>.github.io/ai-sales-agent/`

The workflow in `.github/workflows/deploy-pages.yml` publishes the repository root, where `index.html` lives.

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

## 🎨 Customization

### GitHub Pages Version

Edit the standalone `index.html` file:

**Adding More Offers**: Modify the `ALL_OFFERS` array in the `<script>` section:
```javascript
const ALL_OFFERS = [
    {id: 9, title: "New Product", category: "electronics", 
     price: 500, discount: 20, rating: 4.8},
    // Add more...
];
```

**Modifying UI Styles**: Edit the `<style>` section to customize colors, fonts, and layout.

**Extending Query Parsing**: Modify the `parseQuery()` function to recognize more keywords and patterns.

### Python Backend Version

**Adding More Offers**: Edit `backend.py` and add items to the `OFFERS` list.

**Modifying UI Styles**: Edit `templates/index.html` to customize the interface.

**Extending Agent Logic**: Edit `agent/ai_agent_llm_autonomous_web.py` to add more decision-making logic.

## 💻 Technologies Used

**GitHub Pages Version:**
- Pure HTML, CSS, and JavaScript
- No dependencies or build tools
- Works offline after first load

**Python Backend Version:**

- **FastAPI**: Modern web framework for Python
- **Jinja2**: Template engine for HTML
- **Vanilla JavaScript**: No frontend framework dependencies
- **OpenAI API**: Optional LLM integration for better parsing
- **Uvicorn**: ASGI server for running the applications

## License

MIT License - feel free to use and modify for your projects!

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
