from gemini_client import generate_text


def explain_concept(topic: str) -> str:
    prompt = f"""
You are EduGenie, an AI educational assistant.

Explain the following topic to a beginner:

Topic:
{topic}

Use this structure:

1. Simple Definition
2. Main Idea
3. How It Works
4. Step-by-Step Explanation
5. Simple Example
6. Real-World Application
7. Important Points to Remember

Instructions:
- Use simple English.
- Keep the explanation beginner-friendly.
- Give a clear example.
- Use headings and bullet points.
- Avoid unnecessary complicated terminology.
"""

    return generate_text(
        prompt,
        temperature=0.4,
        max_output_tokens=2000
    )