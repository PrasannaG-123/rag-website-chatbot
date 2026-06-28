from google import genai
import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Create Gemini client
client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def generate_answer(context, question):

    prompt = f"""
You are an AI assistant.

Answer ONLY using the website context.

Rules:
1. Answer only from context.
2. If answer not found, say:
   I could not find this information on the website.
3. Do not invent information.

WEBSITE CONTEXT:
{context}

QUESTION:
{question}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text