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
        else:
            plan_name = final_state.plan.name if final_state.plan else None
            project_root = (
                str(final_state.project_root)
                if final_state.project_root
                else None
            )
            completed_files = final_state.completed_files
            status = final_state.status

        return GenerateResponse(
            status=status,
            project_name=plan_name,
            project_root=project_root,
            completed_files=completed_files,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
