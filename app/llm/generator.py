import os
from dotenv import load_dotenv
from groq import Groq

from app.llm.prompt import PROMPT_TEMPLATE

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


class LLMGenerator:

    @staticmethod
    def generate(document_text: str):

        prompt = PROMPT_TEMPLATE.format(
            document=document_text
        )

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.2
        )

        print("========== LLM OUTPUT ==========")
        print(response.choices[0].message.content)
        print("================================")

        return response.choices[0].message.content