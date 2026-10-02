from gemini_client import generate_text


def get_learning_recommendations(topic: str) -> str:
    prompt = f"""
You are EduGenie, an AI educational assistant.

Create a learning path for a student who wants to learn the following topic:

Topic:
{topic}

Create a beginner-friendly learning path.

Include:

1. Beginner Level
2. Intermediate Level
3. Advanced Level
4. Suggested Timeline
5. Practice Activities
6. Important Topics to Learn
7. Final Project or Application

Instructions:
- Use simple English.
- Start from basic concepts.
- Progress gradually from beginner to advanced.
- Use headings and bullet points.
- Give practical examples.
- Make the plan suitable for a student.
"""

    return generate_text(
        prompt,
        temperature=0.4,
        max_output_tokens=2000
    )