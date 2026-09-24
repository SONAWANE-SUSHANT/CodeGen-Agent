from agent.core.llm import llm
from agent.core.state import GraphState, ReviewFeedback
from agent.prompts.reviewer import reviewer_prompt
from agent.tools.filesystem import list_files, read_file


class Reviewer:
    """Evaluates the generated project for correctness, completeness, and consistency."""

    def run(self, state: GraphState) -> GraphState:
        if state.plan is None:
            raise ValueError("Plan missing before review.")

        if state.project_root is None:
            raise ValueError("Project root missing before review.")

        # Gather all files in project root
        file_contents = []
        for filepath in list_files(state.project_root):
            content = read_file(state.project_root, filepath)
            file_contents.append(f"=== {filepath} ===\n{content}")

        combined_code = "\n\n".join(file_contents)

        reviewer = llm.with_structured_output(ReviewFeedback)

        prompt = reviewer_prompt(
            user_prompt=state.user_prompt,
            project_name=state.plan.name,
            tech_stack=state.plan.techstack,
            features=state.plan.features,
            project_files_content=combined_code,
            iteration=state.iteration_count + 1,
        )

        feedback = reviewer.invoke(prompt)

        print("\n" + "=" * 60)
        print(f"CODE REVIEW (Iteration {state.iteration_count + 1})")
        print("=" * 60)
        print(f"Approved : {'✓ YES' if feedback.is_approved else '✗ NO'}")
        print(f"Summary  : {feedback.summary}")

        if feedback.issues:
            print("\nIssues Identified:")
            for idx, issue in enumerate(feedback.issues, start=1):
                print(f"  {idx}. [{issue.filepath}] {issue.issue}")
                print(f"     Fix: {issue.fix_instruction}")

        state.review_feedback = feedback

        if feedback.is_approved:
            state.status = "completed"
        else:
            state.status = "needs_revision"

        return state
