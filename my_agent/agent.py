from typing import TypedDict

from langgraph.graph import StateGraph, END
from langgraph.types import interrupt, Command
from langgraph.prebuilt.interrupt import HumanInterruptConfig, HumanInterrupt

class State(TypedDict):
    message: str
    some_text: str
    summary: dict
    

# print(graph.invoke(Command(resume="Edited text"), config=config)) 
# > {'some_text': 'Edited text'}

def node_1(state: State) -> dict:
    return {"summary": {"title": "this is title", "desc": "this is description."}}

def node_2(state: State) -> dict:
    return {"message": "processed message"}

def node_3(state: State) -> dict:
    # value = interrupt( 
    #     {
    #         "some_text": "output text"
    #     }
    # )
    interrupt_config = {
        "allow_accept": True,
        "allow_edit": True,
        "allow_respond": True,
    }
    request: HumanInterrupt = {
        "action_request": {
            "action": "run_command",
            "args": "tool_input"
        },
        "config": interrupt_config,
        "description": "test desc"
    }
    value = interrupt([request])
    return {
        "some_text": value 
    }

workflow = StateGraph(State)

workflow.add_node("node_1", node_1)
workflow.add_node("node_2", node_2)
workflow.add_node("node_3", node_3)

workflow.set_entry_point("node_1")

workflow.add_edge("node_1", "node_2")
workflow.add_edge("node_2", "node_3")
workflow.add_edge("node_3", END)


graph = workflow.compile()

if __name__ == "__main__":
    result = graph.invoke({"message": "Hello"})
    print(f"Final result: {result}")
