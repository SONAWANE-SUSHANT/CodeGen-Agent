from pathlib import Path
from collections import defaultdict
from typing import List
import re

from agent.states import ImplementationTask

WORKSPACE = Path("workspace")


def slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[-\s]+", "-", text)
    return text


def create_project(plan_name: str) -> Path:
    WORKSPACE.mkdir(exist_ok=True)

    project_root = WORKSPACE / slugify(plan_name)
    project_root.mkdir(parents=True, exist_ok=True)

    return project_root


def absolute_path(project_root: Path, relative_path: str) -> Path:
    return project_root / relative_path


def ensure_parent_exists(path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)


def read_file(project_root: Path, filepath: str) -> str:
    file = absolute_path(project_root, filepath)

    if not file.exists():
        return ""

    return file.read_text(encoding="utf-8")


def write_file(project_root: Path, filepath: str, content: str):
    file = absolute_path(project_root, filepath)

    ensure_parent_exists(file)

    file.write_text(content, encoding="utf-8")


def create_empty_files(project_root: Path, files: List[str]):
    for file in files:

        path = absolute_path(project_root, file)

        ensure_parent_exists(path)

        if not path.exists():
            path.touch()


def list_files(project_root: Path) -> List[str]:
    files = []

    for path in project_root.rglob("*"):
        if path.is_file():
            files.append(str(path.relative_to(project_root)))

    return sorted(files)


def file_exists(project_root: Path, filepath: str) -> bool:
    return absolute_path(project_root, filepath).exists()


def delete_file(project_root: Path, filepath: str):
    file = absolute_path(project_root, filepath)

    if file.exists():
        file.unlink()


def group_tasks_by_file(
    tasks: list[ImplementationTask],
) -> dict[str, list[str]]:
    """
    Groups tasks by filepath.
    """

    grouped = defaultdict(list)

    for task in tasks:
        grouped[task.filepath].append(
            task.task_description
        )

    return dict(grouped)

def read_project_context(
    project_root: Path,
    target_file: str,
) -> str:
    """
    Returns the contents of all generated files except the
    file currently being generated.
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