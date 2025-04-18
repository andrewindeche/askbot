from pydantic import BaseModel
from typing import List

class RecipeRequest(BaseModel):
    """
    Model for generating requests for recipe
    
    Attribute for type checking and describing dish that is looked for in a recipe
    """
    prompt: str

class RecipeResponse(BaseModel):
    """
    Model for generating responses for the recipe
    Attributes:
        title (str): response with a title of string type
        ingredients (List[str]): response with a list of ingredients
        instructions (List[str]): response with step by step instructions
        image_url (str): URL for an image of the dish
    """
    title: str
    ingredients: List[str]
    instructions: List[str]
    image_url: str
