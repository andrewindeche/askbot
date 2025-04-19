def format_recipe_prompt(prompt: str) -> str:
    """
    Formats a recipe prompt for structured LLM queries.

    Args:
        prompt (str): The recipe request from the user.

    Returns:
        str: A formatted prompt string for the AI.
    """
    return f"""Generate a recipe for: {prompt}

Respond in the following format:

Title
- Ingredient 1
- Ingredient 2
1. Step one
2. Step two
...
"""
