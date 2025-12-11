from langgraph.graph import StateGraph, END
from typing import TypedDict, Optional

# Define the agent's state structure
class AgentState(TypedDict):
    remaining_items: list[str]
    collected_data: dict[str, str]
    current_prompt: Optional[str]
    current_response: Optional[str]

def get_next_prompt(state: AgentState) -> dict:
    """Node: Get prompt for next item in list"""
    if not state["remaining_items"]:
        return {"current_prompt": None}
    
    next_item = state["remaining_items"][0]
    return {
        "current_prompt": f"Please provide your {next_item}: ",
        "current_response": None
    }

def process_user_input(state: AgentState) -> dict:
    """Node: Process user input and update state"""
    if not state["remaining_items"]:
        return {}
    
    # Simulate user input (in real scenario, this would come from external source)
    user_response = input(state["current_prompt"])
    
    return {
        "current_response": user_response,
        "current_prompt": None
    }

def update_agent_state(state: AgentState) -> dict:
    """Node: Update state with collected response"""
    if not state["remaining_items"]:
        return {}
    
    current_item = state["remaining_items"].pop(0)
    return {
        "collected_data": {**state["collected_data"], current_item: state["current_response"]},
        "remaining_items": state["remaining_items"],
        "current_response": None
    }

def should_continue(state: AgentState) -> str:
    """Conditional edge: Check if we should continue processing"""
    return "continue" if state["remaining_items"] else "end"

# Create workflow
workflow = StateGraph(AgentState)

# Add nodes
workflow.add_node("get_prompt", get_next_prompt)
workflow.add_node("get_input", process_user_input)
workflow.add_node("update_state", update_agent_state)

# Set up edges
workflow.set_entry_point("get_prompt")
workflow.add_edge("get_prompt", "get_input")
workflow.add_edge("get_input", "update_state")
workflow.add_conditional_edges(
    "update_state",
    should_continue,
    {
        "continue": "get_prompt",
        "end": END
    }
)

# Compile the graph
agent = workflow.compile()

# Example usage
if __name__ == "__main__":
    # Initialize state
    initial_state = AgentState(
        remaining_items=["name", "age", "email", "favorite color"],
        collected_data={},
        current_prompt=None,
        current_response=None
    )
    
    # Run the agent
    final_state = agent.invoke(initial_state)
    
    # Show results
    print("\nThank you! Here's what we collected:")
    for key, value in final_state["collected_data"].items():
        print(f"- {key}: {value}")