from agent.states import Plan


def planner_prompt(user_request: str) -> str:
    return f"""
You are an expert software architect.

Design a software project based on the user's request.

Return:

- Project name
- Description
- Tech stack
- Features
- Files required

User Request:

{user_request}
"""


def architect_prompt(plan: Plan) -> str:

    features = "\n".join(
        f"- {feature}"
        for feature in plan.features
    )

    files = "\n".join(
        f"- {file.path}: {file.purpose}"
        for file in plan.files
    )

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


def coder_prompt(
    project_name: str,
    project_description: str,
    tech_stack: str,
    features: list[str],
    tasks: list[str],
    filepath: str,
    existing_content: str,
    project_context: str,
    project_files: list[str],
    completed_tasks: list[str],
) -> str:

    feature_text = "\n".join(
        f"- {f}"
        for f in features
    )

    file_text = "\n".join(
        f"- {f}"
        for f in project_files
    )

    completed = (
        "\n".join(
            f"- {t}"
            for t in completed_tasks
        )
        if completed_tasks
        else "None"
    )

    task_text = "\n".join(
        f"- {t}"
        for t in tasks
    )

    if not existing_content.strip():
        existing_content = "(empty file)"

    return f"""
You are an expert senior software engineer.

Your job is to generate ONE project file.

Project

Name:
{project_name}

Description:
{project_description}

Tech Stack:
{tech_stack}

Features

{feature_text}

Project Files

{file_text}

Existing Project

{project_context}

Completed Tasks

{completed}

Tasks To Implement

{task_text}

Target File

{filepath}

Current File

{existing_content}

Rules

- Use the Existing Project section to stay consistent with the rest of the project.
- Reuse the same HTML ids, CSS class names, function names, and file structure whenever appropriate.
- Update ONLY the target file.
- Return ONLY the COMPLETE updated file.
- Never explain your answer.
- Never use markdown.
- Never wrap your answer inside ```.

Return only the file contents.
"""