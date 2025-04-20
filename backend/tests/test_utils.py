import responses
import requests

@responses.activate
def test_image_url_mock():
    """
    Test that mocks an external image URL request.
    """
    mock_image_url = "https://via.placeholder.com/300"
    responses.add(
        responses.GET,
        mock_image_url,
        json={"image_url": mock_image_url},
        status=200
    )
    response = requests.get(mock_image_url)
    assert response.status_code == 200
    assert response.json()['image_url'] == mock_image_url
    