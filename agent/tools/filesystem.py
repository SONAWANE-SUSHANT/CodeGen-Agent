import re
from collections import defaultdict
from pathlib import Path
from typing import List

from agent.core.state import ImplementationTask

WORKSPACE = Path("workspace")


def slugify(text: str) -> str:
    """Sanitize and format a project name into a clean directory slug."""
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[-\s]+", "-", text)
    return text


def create_project(plan_name: str) -> Path:
    """Create project workspace folder based on plan name."""
    WORKSPACE.mkdir(exist_ok=True)

    project_root = WORKSPACE / slugify(plan_name)
    project_root.mkdir(parents=True, exist_ok=True)

    return project_root


def absolute_path(project_root: Path, relative_path: str) -> Path:
    """Resolve full path inside project root."""
    return project_root / relative_path


def ensure_parent_exists(path: Path) -> None:
    """Create parent directories if they do not exist."""
    path.parent.mkdir(parents=True, exist_ok=True)


def read_file(project_root: Path, filepath: str) -> str:
    """Read the content of a file in the project workspace."""
    file = absolute_path(project_root, filepath)

    if not file.exists():
        return ""

    return file.read_text(encoding="utf-8")


def write_file(project_root: Path, filepath: str, content: str) -> None:
    """Write text content to a target file in the project workspace."""
    file = absolute_path(project_root, filepath)

    ensure_parent_exists(file)

    file.write_text(content, encoding="utf-8")


def create_empty_files(project_root: Path, files: List[str]) -> None:
    """Pre-touch files defined in the project architecture."""
    for file in files:
        path = absolute_path(project_root, file)
        ensure_parent_exists(path)

        if not path.exists():
            path.touch()


def list_files(project_root: Path) -> List[str]:
    """List all relative file paths currently within the project."""
    files = []

    for path in project_root.rglob("*"):
        if path.is_file():
            files.append(str(path.relative_to(project_root)))

    return sorted(files)


def file_exists(project_root: Path, filepath: str) -> bool:
    """Check if file exists in the project workspace."""
    return absolute_path(project_root, filepath).exists()


def delete_file(project_root: Path, filepath: str) -> None:
    """Remove a file from the project workspace if it exists."""
    file = absolute_path(project_root, filepath)

    if file.exists():
        file.unlink()


def group_tasks_by_file(
    tasks: list[ImplementationTask],
) -> dict[str, list[str]]:
    """Groups implementation tasks by filepath."""
    grouped = defaultdict(list)

    for task in tasks:
        grouped[task.filepath].append(task.task_description)

    return dict(grouped)


def read_project_context(
    project_root: Path,
    target_file: str,
) -> str:
    """
    Returns the contents of all generated files except the
    file currently being generated to provide coherent context.
    """
    sections = []

    for filepath in list_files(project_root):
        if filepath == target_file:
            continue

        content = read_file(project_root, filepath)

        if not content.strip():
            continue

        sections.append(
            f"========== {filepath} ==========\n"
            f"{content}"
        )

    if not sections:
        return "No project files have been generated yet."

    return "\n\n".join(sections)
