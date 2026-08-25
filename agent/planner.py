from agent.llm import llm
from agent.prompts import planner_prompt
from agent.states import GraphState, Plan


class Planner:

    def run(self, state: GraphState) -> GraphState:
        """
        Generates the high-level project plan.
        """

        planner = llm.with_structured_output(Plan)

        plan = planner.invoke(
            planner_prompt(state.user_prompt)
        )

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