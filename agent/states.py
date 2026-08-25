from pathlib import Path

from pydantic import BaseModel, Field


# ---------- Planner Models ----------


class File(BaseModel):
    path: str = Field(description="Relative path of the file.")
    purpose: str = Field(description="Why this file exists.")


class Plan(BaseModel):
    name: str
    description: str
    techstack: str
    features: list[str]
    files: list[File]


# ---------- Architect Models ----------


class ImplementationTask(BaseModel):
    filepath: str
    task_description: str


class TaskPlan(BaseModel):
    implementation_steps: list[ImplementationTask]


# ---------- Graph State ----------


class GraphState(BaseModel):
    user_prompt: str

    plan: Plan | None = None
    task_plan: TaskPlan | None = None

    project_root: Path | None = None

    completed_files: list[str] = []
    completed_tasks: list[str] = []

    current_task_index: int = 0

    status: str = "planning"
