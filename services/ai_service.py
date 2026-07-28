from pydoc import text

from google import genai
from config import GEMINI_API_KEY
from config import GEMINI_MODEL


class AIService:

    def __init__(self):
        self.client = genai.Client(api_key=GEMINI_API_KEY)

    def generate_answer(self, prompt: str) -> str:
        """
        Sends the prompt to Gemini and returns the generated answer.
        """

        response = self.client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt
        )
        text = response.text

        if text:
            return text.strip()

        return "I couldn't generate a response."