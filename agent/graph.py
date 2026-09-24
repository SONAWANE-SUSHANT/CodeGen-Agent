from langgraph.graph import END, START, StateGraph

from agent.core.state import GraphState
from agent.nodes.architect import Architect
from agent.nodes.coder import Coder
from agent.nodes.planner import Planner

# Node instances
planner = Planner()
architect = Architect()
coder = Coder()


def planner_node(state: GraphState) -> GraphState:
    return planner.run(state)


def architect_node(state: GraphState) -> GraphState:
    return architect.run(state)


def coder_node(state: GraphState) -> GraphState:
    return coder.run(state)


# Build multi-agent orchestration graph
builder = StateGraph(GraphState)

builder.add_node("planner", planner_node)
builder.add_node("architect", architect_node)
builder.add_node("coder", coder_node)

builder.add_edge(START, "planner")
builder.add_edge("planner", "architect")
builder.add_edge("architect", "coder")
builder.add_edge("coder", END)

graph = builder.compile()