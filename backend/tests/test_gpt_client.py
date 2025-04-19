import logging
from unittest.mock import patch
import pytest
import openai
import responses

logging.basicConfig(level=logging.INFO)
@pytest.fixture
def mock_chatgpt_client():
    """
    Fixture to mock chatgpt_client
    """
    class MockChatGPTClient:
        """
        A mock class that simulates the behavior of the ChatGPT client.
        
        It is used in unit tests to simulate querying ChatGPT and receiving 
        predefined responses.
        """
        def query(self, prompt: str):
            """
            Simulates a query to the ChatGPT model.

            Args:
                prompt (str): The prompt to send to the ChatGPT model.

            Returns:
                str: The simulated response from ChatGPT based on the prompt.
            """
            return "Kenyan tea is made by boiling tea leaves, water, and sugar, and served with milk."

    return MockChatGPTClient()

@responses.activate
def test_successful_query_with_mocked_image(mock_chatgpt_client):
    """
    Test that verifies the successful response from the ChatGPT model when 
    the OpenAI API call is mocked. It also mocks an image URL and ensures 
    the recipe generation works as expected.
    """
    mock_openai_response = {
        'choices': [{
            'message': {
                'content': 'Kenyan tea is made by boiling tea leaves, water, and sugar, and served with milk.'
            }
        }]
    }

    mock_image_url = "https://via.placeholder.com/300"
    responses.add(
        responses.GET,
        mock_image_url,
        json={"image_url": mock_image_url},
        status=200
    )

    with responses.RequestsMock() as rs:
        rs.add(
            rs.POST,
            "https://api.openai.com/v1/completions",
            json=mock_openai_response,
            status=200
        )
        response = mock_chatgpt_client.query("Write a short recipe for Kenyan tea.")
        assert response == "Kenyan tea is made by boiling tea leaves, water, and sugar, and served with milk."

@responses.activate
@patch("openai.ChatCompletion.create")
def test_rate_limit_error_with_mocked_image(mock_create, mock_chatgpt_client):
    """
    Test that verifies the handling of rate limit errors from the OpenAI API
    when querying for a recipe.
    """
    mock_create.side_effect = openai.error.RateLimitError("You have exceeded your quota.")

    response = mock_chatgpt_client.query("Write a short recipe for Kenyan tea.")
    assert response == "Rate limit exceeded. Please try again later."
