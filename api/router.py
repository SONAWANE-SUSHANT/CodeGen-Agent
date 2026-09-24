from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from agent.core.state import GraphState
from agent.graph import graph
from config.settings import settings

router = APIRouter()


class GenerateRequest(BaseModel):
    prompt: str = Field(
        ...,
        description="Prompt describing the application to generate.",
        example="Create a modern calculator with scientific operations and dark theme.",
    )


class GenerateResponse(BaseModel):
    status: str
    project_name: str | None = None
    project_root: str | None = None
    completed_files: list[str] = []
    review_approved: bool | None = None
    review_summary: str | None = None
    iteration_count: int = 0


@router.get("/health", tags=["health"])
def health_check() -> dict[str, str]:
    return {
        "status": "ok",
        "service": "codegen-agent",
        "environment": settings.app_env,
    }


@router.post("/generate", response_model=GenerateResponse, tags=["agent"])
def generate_project(req: GenerateRequest) -> GenerateResponse:
    """Generate a full code project from a user prompt using the multi-agent pipeline."""
    try:
        initial_state = GraphState(user_prompt=req.prompt)
        final_state = graph.invoke(initial_state)

        if isinstance(final_state, dict):
            plan = final_state.get("plan")
            plan_name = (
                plan.name
                if hasattr(plan, "name")
                else (plan.get("name") if isinstance(plan, dict) else None)
            )
            project_root = (
                str(final_state.get("project_root"))
                if final_state.get("project_root")
                else None
            )
            completed_files = final_state.get("completed_files", [])
            status = final_state.get("status", "completed")
            feedback = final_state.get("review_feedback")
            review_approved = (
                feedback.is_approved
                if hasattr(feedback, "is_approved")
                else (
                    feedback.get("is_approved")
                    if isinstance(feedback, dict)
                    else None
                )
            )
            review_summary = (
                feedback.summary
                if hasattr(feedback, "summary")
                else (
                    feedback.get("summary")
                    if isinstance(feedback, dict)
                    else None
                )
            )
            iteration_count = final_state.get("iteration_count", 0)
        else:
            plan_name = final_state.plan.name if final_state.plan else None
            project_root = (
                str(final_state.project_root)
                if final_state.project_root
                else None
            )
            completed_files = final_state.completed_files
            status = final_state.status
            review_approved = (
                final_state.review_feedback.is_approved
                if final_state.review_feedback
                else None
            )
            review_summary = (
                final_state.review_feedback.summary
                if final_state.review_feedback
                else None
            )
            iteration_count = final_state.iteration_count

        return GenerateResponse(
            status=status,
            project_name=plan_name,
            project_root=project_root,
            completed_files=completed_files,
            review_approved=review_approved,
            review_summary=review_summary,
            iteration_count=iteration_count,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
