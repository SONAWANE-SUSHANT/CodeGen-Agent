"""
Backward-compatibility bridge for agent.llm.
LLM instance has moved to agent.core.llm.
"""
from agent.core.llm import llm

__all__ = ["llm"]