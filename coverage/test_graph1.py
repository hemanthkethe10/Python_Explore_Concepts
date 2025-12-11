import os
from typing import TypedDict, Optional, List, Dict, Any
from uuid import uuid4
from fastapi import FastAPI, HTTPException
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.mongodb import MongoDBSaver
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel
from datetime import datetime, timedelta
from langgraph.checkpoint.base import Checkpoint, CheckpointMetadata

app = FastAPI()

# Configuration
class Config:
    MONGODB_URI = os.getenv("MONGODB_URI", "mongodb+srv://sentinel-ai-user:4JlNDabpekHtCkoq@bb-non-prod.i8ab8.mongodb.net/?retryWrites=true&w=majority")
    DB_NAME = "sentinel_ai"
    COLLECTION_NAME = "checkpoints"
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    OPENAI_MODEL = "gpt-3.5-turbo"
    SESSION_TTL_HOURS = 24

# Initialize components
chat_model = ChatOpenAI(
    api_key=Config.OPENAI_API_KEY,
    model=Config.OPENAI_MODEL,
    temperature=0
)

mongo_client = AsyncIOMotorClient(Config.MONGODB_URI)
collection = mongo_client[Config.DB_NAME][Config.COLLECTION_NAME]
checkpointer = MongoDBSaver(collection, ttl=86400)

# State definition
class AgentState(TypedDict):
    remaining_items: List[str]
    collected_data: Dict[str, str]
    conversation_history: List[Dict[str, str]]
    current_prompt: Optional[str]
    awaiting_input: bool
    last_active: datetime

# Graph nodes
def generate_prompt(state: AgentState) -> Dict:
    if not state["remaining_items"]:
        return {"awaiting_input": False}
    
    next_item = state["remaining_items"][0]
    history = "\n".join(
        f"{msg['role']}: {msg['content']}" 
        for msg in state["conversation_history"]
    )
    
    message = chat_model.invoke([
        SystemMessage(content=f'''
            Generate a conversational prompt to request {next_item}.
            Conversation history: {history}
            Keep it friendly and concise.
        '''),
        HumanMessage(content="Create the prompt")
    ])
    
    return {
        "current_prompt": message.content,
        "awaiting_input": True,
        "conversation_history": [
            *state["conversation_history"],
            {"role": "system", "content": f"Requesting {next_item}"},
            {"role": "assistant", "content": message.content}
        ],
        "last_active": datetime.now()
    }

def process_input(state: AgentState) -> Dict:
    user_input = state.get("current_response", "")
    current_item = state["remaining_items"][0]
    
    validation = chat_model.invoke([
        SystemMessage(content=f'''
            Validate this {current_item}: {user_input}.
            Return VALID or explain the issue.
            Be strict but friendly.
        '''),
        HumanMessage(content="Validate the input")
    ])
    
    if "VALID" in validation.content.upper():
        return {
            "collected_data": {
                **state["collected_data"], 
                current_item: user_input
            },
            "remaining_items": state["remaining_items"][1:],
            "awaiting_input": False,
            "conversation_history": [
                *state["conversation_history"],
                {"role": "user", "content": user_input},
                {"role": "system", "content": "Validation passed"}
            ],
            "last_active": datetime.now()
        }
    else:
        return {
            "current_prompt": f"⚠️ {validation.content}",
            "awaiting_input": True,
            "conversation_history": [
                *state["conversation_history"],
                {"role": "user", "content": user_input},
                {"role": "system", "content": "Validation failed"}
            ],
            "last_active": datetime.now()
        }

def should_continue(state: AgentState) -> str:
    if state["awaiting_input"]:
        return "awaiting_input"
    return "continue" if state["remaining_items"] else "end"

# Build workflow
workflow = StateGraph(AgentState)
workflow.add_node("generate_prompt", generate_prompt)
workflow.add_node("process_input", process_input)
workflow.set_entry_point("generate_prompt")

workflow.add_edge("generate_prompt", "process_input")
workflow.add_conditional_edges(
    "process_input",
    should_continue,
    {
        "continue": "generate_prompt",
        "awaiting_input": END,
        "end": END
    }
)

agent = workflow.compile(checkpointer=checkpointer)

# API Models
class ConversationRequest(BaseModel):
    message: str
    session_id: Optional[str] = None

class ConversationResponse(BaseModel):
    response: str
    session_id: str
    status: str
    collected_data: Dict[str, str]
    required_items: List[str]

class StartRequest(BaseModel):
    items: List[str]  # Add request model for items

# API Endpoints
@app.post("/start", response_model=ConversationResponse)
async def start_conversation(request: StartRequest):
    session_id = str(uuid4())
    
    # Let the workflow initialize state naturally
    result = await agent.ainvoke(
        None,  # No initial input needed
        config={
            "configurable": {
                "thread_id": session_id,
                "initial_state": {
                    "remaining_items": request.items,
                    "collected_data": {},
                    "conversation_history": [],
                    "current_prompt": None,
                    "awaiting_input": False,
                    "last_active": datetime.now()
                }
            }
        }
    )
    
    return ConversationResponse(
        response=result["current_prompt"],
        session_id=session_id,
        status="awaiting_input",
        collected_data=result["collected_data"],
        required_items=result["remaining_items"]
    )

@app.post("/chat", response_model=ConversationResponse)
async def handle_chat(request: ConversationRequest):
    return await process_conversation(
        request.session_id or str(uuid4()), 
        request.message
    )

async def process_conversation(session_id: str, message: str) -> ConversationResponse:
    config = {"configurable": {"thread_id": session_id}}
    
    try:
        # Let LangGraph handle state management
        result = await agent.ainvoke(
            {"current_response": message},
            config=config
        )

        response = ConversationResponse(
            response=result.get("current_prompt", "How can I help you?"),
            session_id=session_id,
            status="awaiting_input" if result["awaiting_input"] else "in_progress",
            collected_data=result["collected_data"],
            required_items=result["remaining_items"]
        )

        return response
    
    except Exception as e:
        await checkpointer.adelete(config)
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/resume/{session_id}", response_model=ConversationResponse)
async def resume_conversation(session_id: str):
    config = {"configurable": {"thread_id": session_id}}
    checkpoint = await checkpointer.aget(config)
    
    if not checkpoint or not checkpoint.get("remaining_items"):
        raise HTTPException(status_code=404, detail="Session not found or completed")
    
    return ConversationResponse(
        response=checkpoint.get("current_prompt", "Please continue your input"),
        session_id=session_id,
        status="awaiting_input",
        collected_data=checkpoint.get("collected_data", {}),
        required_items=checkpoint.get("remaining_items", [])
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)