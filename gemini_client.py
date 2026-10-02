import os
import time

from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()


def get_api_key():
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise RuntimeError(
            "GEMINI_API_KEY is missing. Please add your Gemini API key to the .env file."
        )

    return api_key


def get_model_name():
    return os.getenv(
        "GEMINI_MODEL",
        "gemini-3.8-flash"
    )


def generate_text(
    prompt,
    temperature=0.4,
    max_output_tokens=2048
):
    api_key = get_api_key()

    client = genai.Client(
        api_key=api_key
    )

    max_attempts = 4

    for attempt in range(1, max_attempts + 1):

        try:
            response = client.models.generate_content(
                model=get_model_name(),
                contents=prompt,
                config=types.GenerateContentConfig(
                    max_output_tokens=max_output_tokens
                )
            )

            if not response.text:
                raise RuntimeError(
                    "Gemini returned an empty response."
                )

            return response.text.strip()

        except Exception as error:

            error_text = str(error)

            # Retry temporary Gemini server errors
            if "503" in error_text or "UNAVAILABLE" in error_text:

                if attempt < max_attempts:

                    wait_time = attempt * 5

                    print(
                        f"Gemini temporarily unavailable. "
                        f"Retrying in {wait_time} seconds..."
                    )

                    time.sleep(wait_time)

                else:
                    raise RuntimeError(
                        "Gemini is temporarily unavailable because "
                        "the model is experiencing high demand. "
                        "Please try again after a few minutes."
                    ) from error

            else:
                raise