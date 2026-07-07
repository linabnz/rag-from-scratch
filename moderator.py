import json
import os

from dotenv import load_dotenv
from groq import Groq

from config import MODERATION_MODEL

PROMPT_PATH = "prompts/moderator_prompt.txt"


class Moderator:
    def __init__(self):
        load_dotenv()
        self.client = Groq(api_key=os.environ["GROQ_API_KEY"])
        with open(PROMPT_PATH, encoding="utf-8") as f:
            self.system_prompt = f.read()

    def moderate(self, question):
        response = self.client.chat.completions.create(
            model=MODERATION_MODEL,
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": question},
            ],
        )
        return json.loads(response.choices[0].message.content)
