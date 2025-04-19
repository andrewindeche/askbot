import os
from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from app.routes import recipe

# Initialize FastAPI app
app = FastAPI()

# Include the routes
app.include_router(recipe.router)

@app.get("/")
def home():
    """
    Route for home/default page
    """
    return {"message": "Welcome to the ChatGPT Recipe Generator!"}
