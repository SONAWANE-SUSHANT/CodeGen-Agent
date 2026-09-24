from agent.core.state import Plan


def architect_prompt(plan: Plan) -> str:
    features = "\n".join(f"- {feature}" for feature in plan.features)

    files = "\n".join(f"- {file.path}: {file.purpose}" for file in plan.files)

    return f"""
You are a senior software architect.

Break the project into implementation tasks.

Rules:

- Each task modifies ONE file.
- Order tasks logically.
- Keep tasks small.
- Assume previous tasks are already completed.

Project

Name:
{plan.name}

Description:
{plan.description}

Tech Stack:
{plan.techstack}

Features

{features}

Files

{files}
"""
