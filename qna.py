from gemini_client import generate_text


def answer_question(question: str) -> str:
    prompt = f"""
You are EduGenie, an AI educational assistant.

Answer the student's question clearly and accurately.

Question:
{question}

Instructions:
- Use simple English.
- Explain the answer in an easy-to-understand way.
- Use headings and bullet points when useful.
- Include a simple example.
- Avoid unnecessary technical words.
- Do not invent facts.
"""

    return generate_text(
        prompt,
        temperature=0.3,
        max_output_tokens=1500
    )