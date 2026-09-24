from agent.core.llm import llm
from agent.core.state import GraphState
from agent.prompts.coder import coder_fix_prompt, coder_prompt
from agent.tools.filesystem import (
    create_empty_files,
    create_project,
    group_tasks_by_file,
    list_files,
    read_file,
    read_project_context,
    write_file,
)


def clean_code(code: str | list) -> str:
    if isinstance(code, list):
        code = "".join(getattr(block, "text", str(block)) for block in code)

    code = code.strip()

    if code.startswith("```"):
        lines = code.splitlines()
        lines = lines[1:]
        if lines and lines[-1].startswith("```"):
            lines = lines[:-1]
        code = "\n".join(lines)

    return code.strip()


class Coder:
    """Generates code iteratively and applies fixes based on Reviewer feedback."""

    def run(self, state: GraphState) -> GraphState:
        if state.plan is None:
            raise ValueError("Plan missing.")

        if state.task_plan is None:
            raise ValueError("Task plan missing.")

        # Check if this run is a revision based on Reviewer feedback
        if state.review_feedback and not state.review_feedback.is_approved:
            return self._run_revision(state)

        return self._run_initial_generation(state)

    def _run_initial_generation(self, state: GraphState) -> GraphState:
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

            current_content = read_file(state.project_root, filepath)
            project_context = read_project_context(
                state.project_root, filepath
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
            code = clean_code(response.content)

            write_file(state.project_root, filepath, code)

            if filepath not in state.completed_files:
                state.completed_files.append(filepath)

            state.completed_tasks.extend(tasks)
            print(f"✓ Created {filepath}")

        state.status = "coded"
        return state

    def _run_revision(self, state: GraphState) -> GraphState:
        state.iteration_count += 1
        print("\n" + "=" * 60)
        print(f"CODER APPLYING REVIEW FEEDBACK (Revision {state.iteration_count})")
        print("=" * 60)

        issues = state.review_feedback.issues

        if not issues:
            all_files = list_files(state.project_root)
            issues = [
                type(
                    "AnonymousIssue",
                    (),
                    {
                        "filepath": f,
                        "issue": state.review_feedback.summary,
                        "fix_instruction": "Review and refine file to satisfy the specification.",
                    },
                )()
                for f in all_files
            ]

        for issue in issues:
            filepath = issue.filepath
            print(f"Fixing {filepath}: {issue.issue}")

            current_content = read_file(state.project_root, filepath)
            project_context = read_project_context(
                state.project_root, filepath
            )

            prompt = coder_fix_prompt(
                project_name=state.plan.name,
                filepath=filepath,
                existing_content=current_content,
                issue=issue.issue,
                fix_instruction=issue.fix_instruction,
                project_context=project_context,
            )

            response = llm.invoke(prompt)
            code = clean_code(response.content)

            write_file(state.project_root, filepath, code)
            print(f"✓ Fixed {filepath}")

        state.status = "revised"
        return state
