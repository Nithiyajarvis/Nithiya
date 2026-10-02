from gemini_client import generate_text


def summarize_text(text: str) -> str:
    prompt = f"""
You are EduGenie, an AI educational assistant.

Create a concise and easy-to-understand summary of the following text.

Text:
{text}

Instructions:
- Use simple English.
- Keep the important points.
- Use headings and bullet points when useful.
- Make it suitable for student revision.
- Do not add information that is not present in the text.
"""

    return generate_text(
        prompt,
        temperature=0.3,
        max_output_tokens=1500
    )