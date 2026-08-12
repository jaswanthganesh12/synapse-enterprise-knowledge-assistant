from google import genai

from app.core.config import settings


client = genai.Client(
    api_key=settings.gemini_api_key,
)


SYSTEM_INSTRUCTION = """
You are Synapse, an enterprise knowledge assistant.

Answer questions using ONLY the provided context.

Rules:
1. Do not invent information.
2. If the answer is not present in the context, say:
   "I couldn't find this information in the provided documents."
3. Be concise and factual.
4. Preserve technical terminology from the source.
5. Do not use outside knowledge.
"""


def generate_answer(
    query: str,
    context: str,
) -> str:

    prompt = f"""
{SYSTEM_INSTRUCTION}

USER QUESTION:
{query}

RETRIEVED CONTEXT:
{context}

ANSWER:
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )

    return response.text