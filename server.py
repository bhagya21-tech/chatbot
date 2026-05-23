import sys 
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles 
from fastapi.responses import HTMLResponse, FileResponse 
from pydantic import BaseModel

from src.config import get_config 
from src.memory import ConversationMemory 
from src.client import ChatClient 
from src.profile import load_profile, inject_into_system_prompt 

# App state 
memory: ConversationMemory = None 
client: ChatClient = None 
profile: dict = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Runs once on startup -loads config, profile, history."""
    global memory, client, profile 
    
    try:
        config = get_config()
        
    except ValueError as e:
        print(str(e))
        sys.exit(1)
        
    # Inject user profile into system prompt 
    profile = load_profile()
    config["system_prompt"] = inject_into_system_prompt(config["system_prompt"])
    
    # Init components 
    memory = ConversationMemory()
    loaded = memory.load()
    client = ChatClient(config) 
    
    # Load previous chat history 
    loaded = memory.load()
    name = profile.get("name", "")
    print(f"\n✅ Server ready - {'Profile: ' + name if name else 'No profile'} - {loaded} messages loaded") 
    print(f"🌐 Open http://localhost:8000 in your browser\n") 
    
    yield # server runs here 
    
    # shutdown - save memory 
    memory.save()
    print("\n💾 Chat history saved. Goodbye!")
    
    # FASTAPI APP 
app = FastAPI(lifespan=lifespan)
    
    # server static files (CSS, JS if needed later) 
app.mount("/static", StaticFiles(directory="static"), name="static")
    
    # Request 
class ChatRequest(BaseModel):
    message: str 
        
class ChatResponse(BaseModel):
    reply: str 
    message_count: int
         
# Routes 
@app.get("/", response_class=HTMLResponse)
async def serve_ui():
    """Save the main chat UI.""" 
    with open("static/index.html", "r", encoding="utf-8") as f:
        return f.read()
        
@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Receive a message, return AI reply.""" 
    if not request.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty") 
        
    memory.add_user_message(request.message.strip())
        
    try: 
        reply = client.send(memory)
            
    except Exception as e:
        memory._messages.pop()  # rollback on failure 
        raise HTTPException(status_code=500, detail=str(e))
        
    memory.add_assistant_message(reply)
    memory.save()
        
    return ChatResponse(reply=reply, message_count=memory.message_count())
    
@app.post("/clear")
async def clear_memory():
    """Wipe conversation memory and history file.""" 
    memory.clear()
    memory.save()
    return {"status": "cleared"} 
    
@app.get("\profile")
async def get_profile():
    """Returns user profile for display in the UI.""" 
    return {
        "name": profile.get("name", ""),
        "role": profile.get("role", ""),
        "working_on": profile.get("currently_working_on", "")
        
    }
    
@app.get("\history")
async def get_history():
    """Return full conversation history.""" 
    return {"messages": memory.get_history(), "count": memory.message_count()} 

