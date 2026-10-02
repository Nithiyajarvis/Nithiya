import json
import re

from gemini_client import generate_text


def clean_json_response(text: str) -> str:
    text = text.strip()

    # Remove Markdown code fences such as ```json ... ```
    text = re.sub(r"^```json\s*", "", text, flags=re.IGNORECASE)
    text = re.sub(r"^```\s*", "", text)
    text = re.sub(r"\s*```$", "", text)

    return text.strip()


def generate_quiz(topic: str):
    prompt = f"""
Create a quiz for a student about the following topic:

Topic:
{topic}

Return EXACTLY 3 multiple-choice questions.

Each question must have:
- "question"
- "options" containing exactly 4 options
- "answer" containing the correct option

Return ONLY valid JSON.

Required format:

[
  {{
    "question": "Question 1",
    "options": [
      "Option A",
      "Option B",
      "Option C",
      "Option D"
    ],
    "answer": "Option A"
  }},
  {{
    "question": "Question 2",
    "options": [
      "Option A",
      "Option B",
      "Option C",
      "Option D"
    ],
    "answer": "Option B"
  }},
  {{
    "question": "Question 3",
    "options": [
      "Option A",
      "Option B",
      "Option C",
      "Option D"
    ],
    "answer": "Option C"
  }}
]
"""

    raw_response = generate_text(
        prompt,
        temperature=0.2,
        max_output_tokens=2000
    )

    cleaned_response = clean_json_response(raw_response)

    try:
        quiz = json.loads(cleaned_response)
    except json.JSONDecodeError as exc:
        raise RuntimeError(
            f"Gemini returned invalid quiz JSON: {exc}"
        ) from exc

    if not isinstance(quiz, list):
        raise RuntimeError("Quiz response must be a JSON list.")

    if len(quiz) != 3:
        raise RuntimeError("Quiz must contain exactly 3 questions.")

    for index, item in enumerate(quiz, start=1):
        if not isinstance(item, dict):
            raise RuntimeError(f"Question {index} is not valid.")

        if "question" not in item:
            raise RuntimeError(f"Question {index} is missing 'question'.")

        if "options" not in item:
            raise RuntimeError(f"Question {index} is missing 'options'.")

        if "answer" not in item:
            raise RuntimeError(f"Question {index} is missing 'answer'.")

        if len(item["options"]) != 4:
            raise RuntimeError(
                f"Question {index} must have exactly 4 options."
            )

        if item["answer"] not in item["options"]:
            raise RuntimeError(
                f"Question {index} has an answer that is not in its options."
            )

    return quiz