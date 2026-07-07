import os

from dotenv import load_dotenv
from groq import Groq

from config import LLM_MODEL
from vector_db import VectorDB

PROMPT_PATH = "prompts/rag_prompt.txt"


class RAG:
    def __init__(self, persist_path, chunks=None):
        load_dotenv()
        self.client = Groq(api_key=os.environ["GROQ_API_KEY"])
        self.vector_db = VectorDB(persist_path=persist_path, chunks=chunks)
       

    def _build_system_prompt(self, question):
        with open(PROMPT_PATH, encoding="utf-8") as f:
            template = f.read()

        retrieved = self.vector_db.retrieve(question, n=3)
        chunks_text = "\n".join(f"- {doc}" for doc in retrieved["documents"])
        return template.replace("{{Chunks}}", chunks_text)

    def answer_question(self, question):
        system_prompt = self._build_system_prompt(question)

        response = self.client.chat.completions.create(
            model=LLM_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": question},
            ],
        )
        return response.choices[0].message.content
