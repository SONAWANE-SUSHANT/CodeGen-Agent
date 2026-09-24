"""
Backward-compatibility bridge for agent.reviewer.
Reviewer node has moved to agent.nodes.reviewer.
"""
from agent.nodes.reviewer import Reviewer

__all__ = ["Reviewer"]
