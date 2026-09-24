from agent.core.llm import llm
from agent.core.state import GraphState
from agent.prompts.coder import coder_prompt
from agent.tools.filesystem import (
    create_empty_files,
    create_project,
    group_tasks_by_file,
    list_files,
    read_file,
    read_project_context,
    write_file,
)


class Coder:
    """Generates code iteratively for each file while maintaining cross-file context."""

    def run(self, state: GraphState) -> GraphState:
        if state.plan is None:
            raise ValueError("Plan missing.")

        if state.task_plan is None:
            raise ValueError("Task plan missing.")

        # Create project workspace directory and scaffold files
        if state.project_root is None:
            project_root = create_project(state.plan.name)

            create_empty_files(
                project_root,
                [f.path for f in state.plan.files],
            )

            state.project_root = project_root
            print(f"\nProject created at:\n{project_root}\n")

        grouped_tasks = group_tasks_by_file(
            state.task_plan.implementation_steps
        )

        for filepath, tasks in grouped_tasks.items():
            print("=" * 60)
            print(f"Working on {filepath}")
            print("=" * 60)

            # Read current file if partially written
            current_content = read_file(
                state.project_root,
                filepath,
            )

            # Read all other generated files to provide complete project context
            project_context = read_project_context(
                state.project_root,
                filepath,
            )

            prompt = coder_prompt(
                project_name=state.plan.name,
                project_description=state.plan.description,
                tech_stack=state.plan.techstack,
                features=state.plan.features,
                tasks=tasks,
                filepath=filepath,
                existing_content=current_content,
                project_context=project_context,
                project_files=list_files(state.project_root),
                completed_tasks=state.completed_tasks,
            )

            response = llm.invoke(prompt)
            code = response.content

            if isinstance(code, list):
                code = "".join(
                    getattr(block, "text", str(block)) for block in code
                )

            code = code.strip()

            # Clean markdown code blocks if the model wrapped it
            if code.startswith("```"):
                lines = code.splitlines()
                lines = lines[1:]
                if lines and lines[-1].startswith("```"):
                    lines = lines[:-1]
                code = "\n".join(lines)

            write_file(
                state.project_root,
                filepath,
                code,
            )

            if filepath not in state.completed_files:
                state.completed_files.append(filepath)

            state.completed_tasks.extend(tasks)
            print(f"✓ Updated {filepath}")

        state.status = "completed"
        return state
