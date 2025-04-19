from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from app.routes import recipe
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(recipe.router)

@app.get("/")
def home():
    """
    Route for home/default page
    """
    return {"message": "Welcome to the ChatGPT Recipe Generator!"}
