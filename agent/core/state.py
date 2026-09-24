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


# ---------- Reviewer Models ----------


class FileIssue(BaseModel):
    filepath: str = Field(description="File that needs modification.")
    issue: str = Field(description="Description of what is wrong or missing.")
    fix_instruction: str = Field(description="Explicit instruction on how to fix it.")


class ReviewFeedback(BaseModel):
    is_approved: bool = Field(
        description="True if the code is complete, correct, and high quality. False if issues must be fixed."
    )
    summary: str = Field(description="Summary of the code review.")
    issues: list[FileIssue] = Field(
        default=[], description="List of specific issues found, if any."
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

    review_feedback: ReviewFeedback | None = None
    iteration_count: int = 0
    max_iterations: int = 2

    status: str = "planning"
