import os
import openai
from dotenv import load_dotenv

class OpenAIChat:
    # Singleton class to interact with OpenAI GPT models
    _instance = None

    def __new__(cls):
         # Ensure only one instance of OpenAIChat exists
        if cls._instance is None:
            cls._instance = super(OpenAIChat, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        # Load OpenAI API key from .env file and configure OpenAI client
        try:
            load_dotenv()
            api_key = os.getenv('OPENAI_API_KEY')
            if not api_key:
                raise ValueError("OPENAI_API_KEY is missing in environment variables.")
            openai.api_key = api_key
        except Exception as e:
            raise EnvironmentError(f"OpenAI initialization failed: {e}")

    def summarize(self, content: str) -> str:
        # Generate a summary of the given text using OpenAI GPT-3.5-turbo
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": content}
                ]
            )
            # Return the generated summary text
            return response['choices'][0]['message']['content']
        except Exception as e:
            raise RuntimeError(f"OpenAI summarization failed: {e}")
        finally:
            print("OpenAI model processing complete.")
