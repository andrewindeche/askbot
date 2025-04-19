"""
Import regular expression dependencies.
"""
import re
from backend.app.clients.gpt_client import GeminiClient
from app.utils.recipe_formatter import format_recipe_prompt

class RecipeService:
    """
    Service that generates recipe details based on user prompts
    """

    def __init__(self):
        """
        Initialize recipe service with Gemini client instance
        """
        self.client = GeminiClient()

    def generate(self, user_prompt: str):
        """
        Generate a recipe based on prompt
        user_prompt: a string description of what a user wants
        Returns:
            dictionary containing:title, ingredients, instructions, and an image URL
        """
        prompt = format_recipe_prompt(user_prompt)
        llm_response = self.client.query(prompt)

        lines = llm_response.splitlines()
        title = lines[0]
        ingredients = [line.strip('- ') for line in lines if line.startswith('-')]
        instructions = [line for line in lines if re.match(r'\\d+\\.', line)]
        image_url = f"https://source.unsplash.com/featured/?{user_prompt.replace(' ', '+')}"

        return {
            "title": title,
            "ingredients": ingredients,
            "instructions": instructions,
            "image_url": image_url
        }
