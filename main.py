from fastapi import FastAPI,HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from agent import agent
from pydantic import BaseModel
from typing import Optional
import uuid

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://edgemarket.ai","http://localhost:5174"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["X-Session-ID"],
)

class ChatRequest(BaseModel):
    user_id: Optional[str]=None
    session_id: Optional[str]=None
    query: str

class ChatResponse(BaseModel):
    session_id: str
    response: str

@app.post("/chat")
async def chat(request: ChatRequest):
    session_id = request.session_id or str(uuid.uuid4())

    async def generate():
        try:
            async for chunk in agent.arun(request.query, session_id=session_id, user_id=request.user_id, stream=True):
                if chunk.content:
                    yield chunk.content
        except Exception as e:
            yield f"\n[Error]: {str(e)}"
    try:
        return StreamingResponse(generate(), media_type="text/plain", headers={"X-Session-ID": session_id})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
