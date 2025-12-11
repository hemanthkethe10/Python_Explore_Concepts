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
    MONGODB_URI = os.getenv("MONGODB_URI", "<MONGODB_URI>")
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
collection = mongo_client["sentinel_ai"]["checkpoints"]
checkpointer = MongoDBSaver(
    collection,
    ttl=86400  # Auto-delete after 24 hours
)

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
    
    # Validate input
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

class ConversationRequest(BaseModel):
    query: str

# API Endpoints
@app.post("/start",response_model=ConversationResponse)
async def start_conversation():
    session_id = str(uuid4())
    initial_state = AgentState(
        remaining_items=['name', 'age', 'email'],
        collected_data={},
        conversation_history=[],
        current_prompt=None,
        awaiting_input=False,
        last_active=datetime.now()
    )
    
    await checkpointer.aput(
        {"configurable": {"thread_id": session_id}},
        Checkpoint(
            v=1,
            ts=datetime.now().timestamp(),
            channel_values=initial_state,
            channel_versions={},
            versions_seen={}
        ),
        metadata=CheckpointMetadata,
        new_versions={}
    )
    return await process_conversation(session_id, "")

@app.post("/chat", response_model=ConversationResponse)
async def handle_chat(request: ConversationRequest):
    return await process_conversation(
        request.session_id or str(uuid4()), 
        request.message
    )

async def process_conversation(session_id: str, message: str) -> ConversationResponse:
    config = {"configurable": {"thread_id": session_id}}
    
    try:
        # Get current state
        checkpoint = await checkpointer.aget(config)
        state = checkpoint.channel_values if checkpoint else None
        
        if state and state["remaining_items"] and not state["awaiting_input"]:
            del config["configurable"]["thread_id"]
            state = None
        
        # Handle new message
        if message:
            input_state = AgentState(
                remaining_items=state["remaining_items"] if state else [],
                collected_data=state["collected_data"] if state else {},
                conversation_history=state["conversation_history"] if state else [],
                current_response=message,
                awaiting_input=False,
                last_active=datetime.now()
            )
            
            updated_state = await agent.ainvoke(
                input_state,
                config=config
            )
        else:
            updated_state = await agent.ainvoke(
                state or AgentState(
                    remaining_items=[],
                    collected_data={},
                    conversation_history=[],
                    current_prompt=None,
                    awaiting_input=False,
                    last_active=datetime.now()
                ),
                config=config
            )
        
        # Build response
        response = ConversationResponse(
            response=updated_state.get("current_prompt", "How can I help you?"),
            session_id=session_id,
            status="awaiting_input" if updated_state["awaiting_input"] else "in_progress",
            collected_data=updated_state["collected_data"],
            required_items=updated_state["remaining_items"]
        )
        
        if not updated_state["remaining_items"]:
            await checkpointer.adelete(config)
        else:
            await checkpointer.aput(config, 
                Checkpoint(
                v=1,
                ts=datetime.now().timestamp(),
                channel_values=updated_state,
                channel_versions={},
                versions_seen={}
            ),
            metadata=CheckpointMetadata,
                new_versions={}
        )
            
        return response
    
    except Exception as e:
        await checkpointer.adelete(config)
        raise HTTPException(status_code=500, detail=str(e))

# Resume endpoint
@app.post("/resume/{session_id}", response_model=ConversationResponse)
async def resume_conversation(session_id: str):
    config = {"configurable": {"thread_id": session_id}}
    checkpoint = await checkpointer.aget(config)
    
    if not checkpoint or not checkpoint.channel_values["remaining_items"]:
        raise HTTPException(status_code=404, detail="Session not found or completed")
    
    return ConversationResponse(
        response=checkpoint.channel_values["current_prompt"],
        session_id=session_id,
        status="awaiting_input",
        collected_data=checkpoint.channel_values["collected_data"],
        required_items=checkpoint.channel_values["remaining_items"]
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)