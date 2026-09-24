"""
Backward-compatibility bridge for agent.states.
Core states have moved to agent.core.state.
"""
from agent.core.state import (
    File,
    FileIssue,
    GraphState,
    ImplementationTask,
    Plan,
    ReviewFeedback,
    TaskPlan,
)

__all__ = [
    "File",
    "Plan",
    "ImplementationTask",
    "TaskPlan",
    "FileIssue",
    "ReviewFeedback",
    "GraphState",
]
