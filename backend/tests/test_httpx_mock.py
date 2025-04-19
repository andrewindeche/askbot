from unittest.mock import patch
import pytest
import httpx

@pytest.mark.asyncio
async def test_image_fetching_with_httpx():
    """
    Test that simulates fetching an image URL using `httpx`.
    """
    mock_image_url = "https://via.placeholder.com/300"

    with patch("httpx.AsyncClient.get") as mock_get:
        mock_get.return_value = httpx.Response(200, json={"image_url": mock_image_url})
        async with httpx.AsyncClient() as client:
            response = await client.get(mock_image_url)
            assert response.status_code == 200
            assert response.json()['image_url'] == mock_image_url
            