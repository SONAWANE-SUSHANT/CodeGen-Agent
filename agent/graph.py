from langgraph.graph import END, START, StateGraph

from agent.core.state import GraphState
from agent.nodes.architect import Architect
from agent.nodes.coder import Coder
from agent.nodes.planner import Planner
from agent.nodes.reviewer import Reviewer

# Node instances
planner = Planner()
architect = Architect()
coder = Coder()
reviewer = Reviewer()


def planner_node(state: GraphState) -> GraphState:
    return planner.run(state)


def architect_node(state: GraphState) -> GraphState:
    return architect.run(state)


def coder_node(state: GraphState) -> GraphState:
    return coder.run(state)


def reviewer_node(state: GraphState) -> GraphState:
    return reviewer.run(state)


def should_continue_review(state: GraphState) -> str:
    if state.review_feedback and state.review_feedback.is_approved:
        print("\n>>> Code review passed! Generation finalized.")
        return END

    if state.iteration_count < state.max_iterations:
        print(
            f"\n>>> Reviewer requested fixes. Looping back to Coder (Iteration {state.iteration_count + 1}/{state.max_iterations})..."
        )
        return "coder"

    print(
        f"\n>>> Maximum review iterations reached ({state.max_iterations}). Finalizing generation."
    )
    return END


# Build multi-agent orchestration graph with reviewer feedback loop
builder = StateGraph(GraphState)

builder.add_node("planner", planner_node)
builder.add_node("architect", architect_node)
builder.add_node("coder", coder_node)
builder.add_node("reviewer", reviewer_node)

builder.add_edge(START, "planner")
builder.add_edge("planner", "architect")
builder.add_edge("architect", "coder")
builder.add_edge("coder", "reviewer")

builder.add_conditional_edges(
    "reviewer",
    should_continue_review,
    {
        "coder": "coder",
        END: END,
    },
)

graph = builder.compile()