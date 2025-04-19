from fastapi import APIRouter, HTTPException
from app.clients.gpt_client import ChatGPTClient 
from app.schemas.recipe import RecipeRequest, RecipeResponse
import re

router = APIRouter()
chatgpt = ChatGPTClient()

@router.post("/generate-recipe", response_model=RecipeResponse)
def generate_recipe(request: RecipeRequest):
    """
    Generates a recipe based on a user's prompt using ChatGPT.
    Returns a structured recipe response.
    """
    prompt = request.prompt

    raw_response = chatgpt.query(
        f"""Generate a recipe based on the following description: "{prompt}". 
        Please respond in the following format: 
        Title: <title> 
        Ingredients: 
        - item 1 
        - item 2 
        Instructions: 
        1. step 1 
        2. step 2 
        Image URL: <url to a dish image (use a stock placeholder if unknown)>
        """
    )

    if not raw_response:
        raise HTTPException(status_code=500, detail="Failed to get a response from ChatGPT.")
    
    try:
        # Parse the response for title, ingredients, instructions, and image URL
        title_match = re.search(r"Title:\s*(.+)", raw_response)
        ingredients_match = re.findall(r"- (.+)", raw_response)
        instructions_match = re.findall(r"\d+\. (.+)", raw_response)
        image_url_match = re.search(r"Image URL:\s*(.+)", raw_response)

        title = title_match.group(1) if title_match else "Untitled"
        ingredients = ingredients_match or []
        instructions = instructions_match or []
        image_url = image_url_match.group(1) if image_url_match else "https://via.placeholder.com/300"

        return RecipeResponse(
            title=title,
            ingredients=ingredients,
            instructions=instructions,
            image_url=image_url
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error parsing recipe: {str(e)}")
