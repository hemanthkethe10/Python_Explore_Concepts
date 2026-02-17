from langgraph.graph import StateGraph, END
from typing import TypedDict, Optional
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

# Initialize chat model
chat_model = ChatOpenAI(
    openai_api_key="<YOUR_OPENAI_API_KEY>",
    model="gpt-3.5-turbo",
    temperature=0,
)

class AgentState(TypedDict):
    remaining_items: list[str]
    collected_data: dict[str, str]
    conversation_history: list[dict]
    current_prompt: Optional[str]
    current_response: Optional[str]

def generate_prompt(state: AgentState) -> dict:
    """Generate context-aware prompt using LLM"""
    if not state["remaining_items"]:
        return {"current_prompt": None}
    
    next_item = state["remaining_items"][0]
    history = "\n".join([f"User: {msg.get('user')or''}\nAI: {msg.get('ai') or ''}" 
                       for msg in state["conversation_history"] or []])
    
    message = chat_model.invoke([
        SystemMessage(content=f'''You're a conversational assistant. Generate a natural prompt to request the user's {next_item}. 
                     Consider this conversation history: {history}'''),
        HumanMessage(content="Create a friendly, conversational prompt")
    ])
    
    return {
        "current_prompt": message.content,
        "conversation_history": [
            *state["conversation_history"],
            {"type": "system", "content": f"Requesting {next_item}"}
        ]
    }

def process_response(state: AgentState) -> dict:
    """Process and validate user input with LLM"""
    user_input = state["current_response"]
    current_item = state["remaining_items"][0]
    
    # Validate input
    validation = chat_model.invoke([
        SystemMessage(content=f'''Validate this {current_item} input: {user_input}. 
                     Return 'VALID' or explain the issue.'''),
        HumanMessage(content="Please validate this input")
    ])
    
    if "VALID" in validation.content.upper():
        return {
            "collected_data": {**state["collected_data"], current_item: user_input},
            "remaining_items": state["remaining_items"][1:],
            "conversation_history": [
                *state["conversation_history"],
                {"type": "user", "content": user_input},
                {"type": "system", "content": f"Valid {current_item} received"}
            ]
        }
    else:
        return {
            "current_prompt": f"Validation Error: {validation.content}",
            "conversation_history": [
                *state["conversation_history"],
                {"type": "user", "content": user_input},
                {"type": "system", "content": f"Invalid {current_item}: {validation.content}"}
            ]
        }

def should_continue(state: AgentState) -> str:
    return "continue" if state["remaining_items"] else "end"

# Setup workflow
workflow = StateGraph(AgentState)
workflow.add_node("generate_prompt", generate_prompt)
workflow.add_node("process_response", process_response)
workflow.set_entry_point("generate_prompt")

workflow.add_edge("generate_prompt", "process_response")
workflow.add_conditional_edges(
    "process_response",
    should_continue,
    {"continue": "generate_prompt", "end": END}
)

agent = workflow.compile()

# Usage example
if __name__ == "__main__":
    initial_state = AgentState(
        remaining_items=["name", "age", "email"],
        collected_data={},
        conversation_history=[],
        current_prompt=None,
        current_response=None
    )
    
    # Simulate conversation
    state = initial_state
    while True:
        # Get current state
        state = agent.invoke(state)
        
        if not state["remaining_items"]:
            break
            
        # Simulate user input
        print("\nAI:", state["current_prompt"])
        user_input = input("User: ")
        state["current_response"] = user_input
    
    print("\nCollected Data:")
    for k, v in state["collected_data"].items():
        print(f"{k}: {v}")