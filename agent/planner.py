"""
Backward-compatibility bridge for agent.planner.
Planner node has moved to agent.nodes.planner.
"""
from agent.nodes.planner import Planner

__all__ = ["Planner"]