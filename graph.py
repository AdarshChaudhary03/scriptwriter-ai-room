from langgraph.graph import StateGraph, START, END
from states import ScriptState
from nodes.brainstorm import brainstorm_ideas
from nodes.write_scene import write_scene
from nodes.improve_scene import improve_scene

def build_graph():
    workflow = StateGraph(ScriptState)
    # Add nodes
    workflow.add_node("brainstorm", brainstorm_ideas)
    workflow.add_node("write_scene", write_scene)
    workflow.add_node("improve_scene", improve_scene)

    # Connect edges
    workflow.add_edge(START, "brainstorm")
    workflow.add_edge("brainstorm", "write_scene")
    workflow.add_edge("write_scene", "improve_scene")
    workflow.add_edge("improve_scene", END)

    return workflow
