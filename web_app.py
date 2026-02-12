from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from uuid import uuid4

from agent.mcp_agent_llm_autonomous_web import MCPLLMAgentAutonomousWeb

app = FastAPI(title="AI Offer Web Demo Multi-Turn")
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

agent = MCPLLMAgentAutonomousWeb("http://localhost:8001")

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    # Generate a session token for the browser
    token = str(uuid4())
    return templates.TemplateResponse("index.html", {"request": request, "session_token": token})

@app.post("/api/query")
async def query_agent(request: Request):
    data = await request.json()
    token = data.get("session_token")
    user_input = data.get("query", "")
    if not token:
        return JSONResponse({"error": "Missing session_token"}, status_code=400)
    result = agent.run(token, user_input)
    return JSONResponse(result)
