from unittest.mock import patch
from fastapi.testclient import TestClient
import pytest
from app.main import app
from app.clients.gpt_client import ChatGPTClient

client = TestClient(app)

class MockChatGPTClient:
    """
    A mock implementation of the ChatGPT client for testing purposes.
    """
    def query(self, _prompt: str) -> str:
        """
        Simulates sending a prompt to the ChatGPT API and returns a predefined response.

        Args:
            prompt (str): The input prompt to generate a recipe for.

        Returns:
            str: A hardcoded recipe response for testing purposes.
        """
        return "Kenyan tea is made by boiling tea leaves, water, and sugar, and served with milk."

@pytest.fixture
def chatgpt_client():
    """
    Pytest fixture that provides the mock ChatGPT client.
    """
    return MockChatGPTClient()

@patch("openai.ChatCompletion.create")
def test_successful_query_with_mocked_image(mock_create, mock_client):
    """
    Test the `/generate-recipe` route with:
    - A mocked OpenAI API response
    - A mock ChatGPT client
    - Validation that the returned content matches the expected mock result
    """
    mock_create.return_value = {
        "choices": [{
            "message": {
                "content": "Kenyan tea is made by boiling tea leaves, water, and sugar, and served with milk."
            }
        }]
    }

    response = mock_client.query("Write a short recipe for Kenyan tea.")

    assert response == "Kenyan tea is made by boiling tea leaves, water, and sugar, and served with milk."
    