"""
Backward-compatibility bridge for agent.architect.
Architect node has moved to agent.nodes.architect.
"""
from agent.nodes.architect import Architect

__all__ = ["Architect"]