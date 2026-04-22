from fastapi import FastAPI,HTTPException
from fastapi.responses import StreamingResponse
from agent import agent
from pydantic import BaseModel
from typing import Optional
import uuid

app = FastAPI()

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
        async for chunk in agent.arun(request.query, session_id=session_id, user_id=request.user_id, stream=True):
            if chunk.content:
                yield chunk.content

    try:
        return StreamingResponse(generate(), media_type="text/plain", headers={"X-Session-ID": session_id})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")



# @app.post("/chat", response_model=ChatResponse)
# async def chat(request: ChatRequest):
#     session_id= request.session_id or str(uuid.uuid4())
#     user_id= request.user_id
#     try:
#         response = await agent.arun(request.query, session_id=session_id, user_id=user_id)
#         return ChatResponse(response=response.content,session_id=session_id)
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error: {str(e)}")