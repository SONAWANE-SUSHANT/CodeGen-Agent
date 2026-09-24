from agent.core.llm import llm
from agent.core.state import GraphState, Plan
from agent.prompts.planner import planner_prompt


class Planner:
    """Generates the high-level project plan from the user's initial prompt."""

    def run(self, state: GraphState) -> GraphState:
        planner = llm.with_structured_output(Plan)

        plan = planner.invoke(planner_prompt(state.user_prompt))

        print("\n" + "=" * 60)
        print("PROJECT PLAN")
        print("=" * 60)

        print(f"Name        : {plan.name}")
        print(f"Description : {plan.description}")
        print(f"Tech Stack  : {plan.techstack}")

        print("\nFeatures")
        for feature in plan.features:
            print(f"  • {feature}")

        print("\nFiles")
        for file in plan.files:
            print(f"  • {file.path}")
            print(f"    {file.purpose}")

        state.plan = plan
        state.status = "planned"

        return state
