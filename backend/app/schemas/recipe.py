import json
from typing import List
import redis
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Redis setup
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)

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

def cache_recipe(prompt: str, recipe_data: dict):
    """
    Function that Caches the recipe
    """
    redis_client.setex(f"recipe:{prompt}", 3600, json.dumps(recipe_data))

def get_cached_recipe(prompt: str):
    """
    Function that Retrieves recipe from cache
    """
    cached_data = redis_client.get(f"recipe:{prompt}")
    if cached_data:
        return json.loads(cached_data)
    return None

@app.post("/generate-recipe", response_model=RecipeResponse)
async def generate_recipe(request: RecipeRequest):
    """
    Asyn function to Check if the recipe exists in the cache
    """
    cached_recipe = get_cached_recipe(request.prompt)
    if cached_recipe:
        return cached_recipe
    recipe = RecipeResponse(
        title=f"Recipe for {request.prompt}",
        ingredients=["Ingredient 1", "Ingredient 2", "Ingredient 3"],
        instructions=["Step 1: Do this", "Step 2: Do that"],
        image_url="https://via.placeholder.com/300"
    )
    recipe_data = recipe.dict()
    cache_recipe(request.prompt, recipe_data)
    return recipe
