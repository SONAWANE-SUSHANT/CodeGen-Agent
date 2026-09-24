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
    feature_text = "\n".join(f"- {f}" for f in features)

    file_text = "\n".join(f"- {f}" for f in project_files)

    completed = (
        "\n".join(f"- {t}" for t in completed_tasks)
        if completed_tasks
        else "None"
    )

    task_text = "\n".join(f"- {t}" for t in tasks)

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


def coder_fix_prompt(
    project_name: str,
    filepath: str,
    existing_content: str,
    issue: str,
    fix_instruction: str,
    project_context: str,
) -> str:
    return f"""
You are an expert senior software engineer resolving an issue identified during code review.

Project: {project_name}
Target File: {filepath}

Issue To Fix:
{issue}

Fix Instructions:
{fix_instruction}

Project Context (other files):
{project_context}

Current File Content:
{existing_content}

Rules:
- Apply the fix completely and accurately.
- Keep consistency with the rest of the project files.
- Return ONLY the COMPLETE updated file.
- Never explain your answer.
- Never use markdown.
- Never wrap your answer inside ```.

Return only the file contents.
"""
