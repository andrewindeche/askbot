import os
import logging
from openai import OpenAI
from openai._exceptions import OpenAIError, AuthenticationError, RateLimitError, APIError

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ChatGPTClient:
    """
    A client to interact with OpenAI's GPT models (v1.0.0+).
    """
    def __init__(self, model_name="gpt-3.5-turbo"):
        """
        Initializes the ChatGPTClient.
        """
        if not client.api_key:
            raise ValueError("OPENAI_API_KEY must be set in your environment.")
        self.model_name = model_name
        logger.info("Initialized ChatGPTClient with model: %s", model_name)

    def query(self, prompt: str) -> str:
        """
        Queries the ChatGPT model using the provided prompt and handles errors.
        """
        try:
            gpt_response = client.chat.completions.create(
                model=self.model_name,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=150
            )
            return gpt_response.choices[0].message.content.strip()

        except AuthenticationError as e:
            logger.error("Authentication Error: %s", e)
            return "Authentication failed. Please check your API key."
        except RateLimitError as e:
            logger.error("Rate Limit Error: %s", e)
            return "Rate limit exceeded. Please try again later."
        except APIError as e:
            logger.error("API Error: %s", e)
            return "API error occurred. Please try again later."
        except OpenAIError as e:
            logger.error("OpenAI Error: %s", e)
            return "An OpenAI error occurred. Please try again later."
        except Exception as e:
            logger.error("Unexpected error during query: %s", e)
            return "An unexpected error occurred during query execution."

if __name__ == "__main__":
    chatgpt_client = ChatGPTClient(model_name="gpt-3.5-turbo")
    USER_PROMPT = "Write a short recipe for Kenyan tea."
    response = chatgpt_client.query(USER_PROMPT)
    logger.info(f"ChatGPT Response: {response}")
