from fastapi.testclient import TestClient
from app.main import app
import responses

client = TestClient(app)

@responses.activate
@patch("openai.ChatCompletion.create")
def test_successful_query_with_mocked_image(mock_create, chatgpt_client):
    """
    Test the `/generate-recipe` route of the FastAPI app with a mocked 
    OpenAI API response and a mocked image URL.
    """
    mock_create.return_value = {"choices": [{"message": {"content": "Kenyan tea is made by boiling tea leaves, water, and sugar, and served with milk."
            }
        }]
    }

    response = chatgpt_client.query("Write a short recipe for Kenyan tea.")
    assert response == "Kenyan tea is made by boiling tea leaves, water, and sugar, and served with milk."
    