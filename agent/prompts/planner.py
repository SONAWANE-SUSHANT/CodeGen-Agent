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
