from agent.core.llm import llm
from agent.core.state import GraphState, TaskPlan
from agent.prompts.architect import architect_prompt


class Architect:
    """Decomposes the high-level project plan into ordered implementation tasks per file."""

    def run(self, state: GraphState) -> GraphState:
        if state.plan is None:
            raise ValueError("Planner must run before Architect.")

        architect = llm.with_structured_output(TaskPlan)

        task_plan = architect.invoke(architect_prompt(state.plan))

        print("\n" + "=" * 60)
        print("IMPLEMENTATION PLAN")
        print("=" * 60)

        for index, task in enumerate(
            task_plan.implementation_steps,
            start=1,
        ):
            print(f"\n{index}. {task.filepath}")
            print(task.task_description)

        state.task_plan = task_plan
        state.status = "architected"

        return state
