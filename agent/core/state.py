from pathlib import Path
from pydantic import BaseModel, Field


# ---------- Planner Models ----------


class File(BaseModel):
    path: str = Field(description="Relative path of the file.")
    purpose: str = Field(description="Why this file exists.")


class Plan(BaseModel):
    name: str = Field(description="Name of the generated project.")
    description: str = Field(description="Overview of the project goals.")
    techstack: str = Field(description="Technologies and frameworks used.")
    features: list[str] = Field(description="Key features of the project.")
    files: list[File] = Field(description="List of files to be generated.")


# ---------- Architect Models ----------


class ImplementationTask(BaseModel):
    filepath: str = Field(description="Target file for this implementation task.")
    task_description: str = Field(description="Specific implementation instructions.")


class TaskPlan(BaseModel):
    implementation_steps: list[ImplementationTask] = Field(
        description="Ordered sequence of implementation tasks."
    )


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
