from vertexai.generative_models import GenerativeModel
import google.auth.exceptions

class GeminiClient:
    """
    A client to interact with Google's Gemini LLM using Vertex AI.
    
    Attributes:
        model (GenerativeModel): The generative model used for queries.
    """
    def __init__(self, model_name="gemini-pro"):
        """
        Initializes the GeminiClient with a specified model.
        """
        self.model = GenerativeModel(model_name)

    def query(self, prompt: str) -> str:
        """
        Add type safety and query the Gemini model using the provided prompt
        """
        try:
            llm_response = self.model.generate_content(prompt)
            return llm_response.text
        except google.auth.exceptions.DefaultCredentialsError as e:
            print(f"Authentication Error: {e}")
        except ValueError as e:
            print(f"Invalid Input: {e}")


if __name__ == "__main__":
    client = GeminiClient()
    USER_PROMPT = "Write a short recipe for Kenyan tea."
    response = client.query(USER_PROMPT)
    print(f"Gemini Response: {response}")
    