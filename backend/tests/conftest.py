import pytest

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
        def __init__(self, should_raise=False):
            self.should_raise = should_raise
        def query(self, _prompt: str) -> str:
            """
            Simulates a query to the ChatGPT model.

            Args:
                prompt (str): The prompt to send to the ChatGPT model.

            Returns:
                str: The simulated response from ChatGPT based on the prompt.
            """
            if self.should_raise:
                raise Exception("Rate limit exceeded. Please try again later.")
            return "Kenyan tea is made by boiling tea leaves, water, and sugar, and served with milk."
    return MockChatGPTClient(should_raise=True)
