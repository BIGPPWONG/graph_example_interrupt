from typing import TypedDict

from langgraph.graph import StateGraph, END
from langgraph.types import interrupt, Command

class State(TypedDict):
    message: str
    some_text: str
    summary: dict
    

# print(graph.invoke(Command(resume="Edited text"), config=config)) 
# > {'some_text': 'Edited text'}

def node_1(state: State) -> dict:
    return {"summary": {"title": "this is title", "desc": "this is description."}}


def node_2(state: State) -> dict:
    value = interrupt( 
        {
            "some_text": "output text"
        }
    )
    return {
        "some_text": value 
    }

workflow = StateGraph(State)

workflow.add_node("node_1", node_1)
workflow.add_node("node_2", node_2)

workflow.set_entry_point("node_1")

workflow.add_edge("node_1", "node_2")
workflow.add_edge("node_2", END)

graph = workflow.compile()

if __name__ == "__main__":
    result = graph.invoke({"message": "Hello"})
    print(f"Final result: {result}")
