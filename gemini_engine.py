import google.generativeai as genai
import os

from dotenv import load_dotenv


load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=api_key)

model = genai.GenerativeModel("gemini-2.5-flash")


def generate_answer(question, context):

    prompt = f"""

You are an intelligent website assistant.

Answer ONLY from the website content below.

If answer is not found, say:
"I could not find this information on the website."

WEBSITE CONTENT:

{context}


QUESTION:

{question}


Rules:

1. Give short professional answer
2. Do not dump raw website text
3. Summarize clearly
4. Answer like chatbot

"""

    try:

        response = model.generate_content(prompt)

        return response.text

    except Exception as e:

        return "Error generating answer"