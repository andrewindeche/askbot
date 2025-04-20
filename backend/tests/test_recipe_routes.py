from unittest.mock import patch
from fastapi.testclient import TestClient
import pytest
import responses
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
        if "rate limit" in _prompt:
            raise Exception("Rate limit exceeded. Please try again later.")
        return "Kenyan tea is made by boiling tea leaves, water, and sugar, and served with milk."

@pytest.fixture
def mock_chatgpt_client():
    """
    Pytest fixture that provides the mock ChatGPT client.
    """
    return MockChatGPTClient()

@patch("openai.ChatCompletion.create")
def test_successful_query_with_mocked_image(mock_create, mock_chatgpt_client):
    """
    Test the mocked client returns expected recipe content.
    """
    mock_create.return_value = {
        'choices': [{
            'message': {
                'content': 'Kenyan tea is made by boiling tea leaves, water, and sugar, and served with milk.'
            }
        }]
    }

    result = mock_chatgpt_client.query("Write a short recipe for Kenyan tea.")
    assert result == "Kenyan tea is made by boiling tea leaves, water, and sugar, and served with milk."

    mock_image_url = "https://via.placeholder.com/300"
    responses.add(
        responses.GET,
        mock_image_url,
        json={"image_url": mock_image_url},
        status=200
    )

    response = mock_chatgpt_client.query("Write a short recipe for Kenyan tea.")
    assert response == "Kenyan tea is made by boiling tea leaves, water, and sugar, and served with milk."

@patch("openai.ChatCompletion.create")
def test_rate_limit_error_with_mocked_image(mock_create):
    """
    Test real GPT client throws exception on rate limit.
    """
    mock_create.side_effect = Exception("Rate limit exceeded. Please try again later.")
    client = ChatGPTClient()
    with pytest.raises(Exception, match="Rate limit exceeded. Please try again later."):
        client.query("Write a short recipe for Kenyan tea.")
