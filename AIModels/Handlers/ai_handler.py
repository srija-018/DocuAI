from AIModels.Gemini.gemini import GeminiChat
from AIModels.OpenAI.openai import OpenAIChat

class AIHandler:
    # Singleton class to manage and select between AI models
    _instance = None

    def __new__(cls):
        # Create a single shared instance of AIHandler
        if cls._instance is None:
            try:
                cls._instance = super(AIHandler, cls).__new__(cls)
                cls._instance.gemini = GeminiChat()  # Initialize Gemini model
                cls._instance.openai = OpenAIChat()  # Initialize OpenAI model
            except Exception as e:
                raise RuntimeError(f"Failed to initialize AIHandler: {e}")
        return cls._instance

    def get_model(self, prompt: str):
        # Decide which model to use based on the prompt
        try:
            prompt = prompt.lower()

            if "file" in prompt or "document" in prompt:
                return self.gemini

            else:
                return self.gemini  
            
        except Exception as e:
            raise ValueError(f"Error while selecting model: {e}")
        finally:
            print("Model selection process complete.")
