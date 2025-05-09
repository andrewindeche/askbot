import os
import logging
import openai

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ChatGPTClient:
    """
    A client to interact with OpenAI's GPT models (v1.0.0+).
    """
    def __init__(self, model_name="gpt-3.5-turbo"):
        """
        Initializes the ChatGPTClient and authenticates with OpenAI API.
        """
        try:
            openai.api_key = os.getenv("OPENAI_API_KEY")
            if not openai.api_key:
                raise ValueError("OPENAI_API_KEY must be set in your environment.")
            self.model_name = model_name
            logger.info("Initialized ChatGPTClient with model: %s", model_name)
        except Exception as e:
            logger.error("Error initializing ChatGPT client: %s", e)
            raise


    def query(self, prompt: str) -> str:
        """
        Queries the ChatGPT model using the provided prompt and handles errors.
        """
        try:
            gpt_response = openai.Completion.create(
                model=self.model_name,
                prompt=prompt,
                max_tokens=150
            )
            return gpt_response['choices'][0]['text'].strip()
        except openai.AuthenticationError as e:
            logger.error("Authentication Error: %s", e)
            return "Authentication failed. Please check your API key."
        except openai.RateLimitError as e:
            logger.error("Rate Limit Error: %s", e)
            return "Rate limit exceeded. Please try again later."
        except openai.APIError as e:
            logger.error("API Error: %s", e)
            return "API error occurred. Please try again later."
        except openai.OpenAIError as e:
            logger.error("OpenAI Error: %s", e)
            return "An OpenAI error occurred. Please try again later."
        except Exception as e:
            logger.error("Unexpected error during query: %s", e)
            return "An unexpected error occurred during query execution."


if __name__ == "__main__":
    # Example usage
    client = ChatGPTClient(model_name="gpt-3.5-turbo")
    USER_PROMPT = "Write a short recipe for Kenyan tea."
    response = client.query(USER_PROMPT)
    logger.info(f"ChatGPT Response: {response}")
