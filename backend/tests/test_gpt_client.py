import logging
from unittest.mock import patch
from openai import RateLimitError
import openai
import responses

logging.basicConfig(level=logging.INFO)
@responses.activate
@patch("openai.resources.chat.Completions.create")
def test_successful_query_with_mocked_image(mock_create,mock_chatgpt_client):
    """
    Test that verifies the successful response from the ChatGPT model when 
    the OpenAI API call is mocked. It also mocks an image URL and ensures 
    the recipe generation works as expected.
    """
    responses.assert_all_requests_are_fired = False
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
@patch("openai.resources.chat.Completions.create")
def test_rate_limit_error_with_mocked_image(mock_create, mock_chatgpt_client):
    """
    Test that verifies the handling of rate limit errors from the OpenAI API
    when querying for a recipe.
    """
    mock_create.side_effect = Exception("You have exceeded your quota.")
    response = mock_chatgpt_client.query("Write a short recipe for Kenyan tea.")
    assert response == "Rate limit exceeded. Please try again later."
