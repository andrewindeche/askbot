"""
import os dependency for env variables
"""
import os
from dotenv import load_dotenv

load_dotenv()

google_project = os.getenv("GOOGLE_CLOUD_PROJECT")
google_region = os.getenv("GOOGLE_CLOUD_REGION")
google_credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

from vertexai.generative_models import GenerativeModel

def get_gemini_model(model_name="gemini-pro"):
    """
    Retrieves a Gemini generative model.

    Args:
        model_name (str): The name of the Gemini model to retrieve. Defaults to "gemini-pro".

    Returns:
        GenerativeModel: An instance of the requested Gemini generative model.
    """
    return GenerativeModel(model_name)
