import os
import google.generativeai as genai
from dotenv import load_dotenv

class GeminiChat:
    # Singleton class to interact with Gemini AI
    _instance = None

    def __new__(cls):
        # Ensure only one instance of GeminiChat exists
        if cls._instance is None:
            cls._instance = super(GeminiChat, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        # Load API key from .env and configure Gemini model
        try:
            load_dotenv()
            api_key = os.getenv('GEMINI_API_KEY')
            if not api_key:
                raise ValueError("GEMINI_API_KEY is missing in environment variables.")
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-1.5-flash')
        except Exception as e:
            raise EnvironmentError(f"Gemini initialization failed: {e}")

    def summarize(self, content: str) -> str:
        # Generate a summary for the given text using Gemini
        try:
            response = self.model.generate_content(content)
            return response.text
        except Exception as e:
            raise RuntimeError(f"Gemini summarization failed: {e}")
        finally:
            print("Gemini model processing complete.")
            
    def ask(self, question: str) -> str:
        # Ask a question (wrapper around summarize)
        return self.summarize(question)