import pytest
import responses
from app.clients.gpt_client import ChatGPTClient
import logging

# Setup logger
logging.basicConfig(level=logging.INFO)

@pytest.fixture
def chatgpt_client():
    """
    Fixture to initialize a ChatGPT client for use in tests.
    """
    return ChatGPTClient(model_name="gpt-3.5-turbo")

@responses.activate
def test_successful_query_with_mocked_image(chatgpt_client):
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
        response = chatgpt_client.query("Write a short recipe for Kenyan tea.")
        assert response == "Kenyan tea is made by boiling tea leaves, water, and sugar, and served with milk."

@responses.activate
@patch("openai.ChatCompletion.create")
def test_rate_limit_error_with_mocked_image(mock_create, chatgpt_client):
    mock_create.side_effect = openai.error.RateLimitError("You have exceeded your quota.")

    response = chatgpt_client.query("Write a short recipe for Kenyan tea.")
    assert response == "Rate limit exceeded. Please try again later."
