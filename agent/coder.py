"""
Backward-compatibility bridge for agent.coder.
Coder node has moved to agent.nodes.coder.
"""
from agent.nodes.coder import Coder

__all__ = ["Coder"]