from openai import AsyncOpenAI, OpenAIError, RateLimitError, APIConnectionError
import os
from dotenv import load_dotenv

load_dotenv()  # Load .env variables

language_mapping = {
    "en": "English",
    "es": "Spanish",
    "fr": "French",
    "de": "German",
    "it": "Italian",
    "pt": "Portuguese",
    "zh": "Chinese",
    "ja": "Japanese",
    "ko": "Korean",
    "ur": "Urdu",
    "hi": "Hindi",
    "ar": "Arabic",
    "ru": "Russian",  # Add more languages as needed
}


async def translate_message(text: str, target_lang: str) -> str:
    prompt = (
        f"Translate the following message to {language_mapping.get(target_lang)}. "
        f"Preserve medical terms and keep the tone clear and professional.\n\n"
        f"Message: \"{text}\""
    )
    print("Prompt is:", prompt)

    try:
        client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        # Use the OpenAI API to get the translation
        response = await client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2
        )
        translation = response.choices[0].message.content.strip()
        print("Translation is:", translation)
        return translation

    except APIConnectionError:
        print("Invalid OpenAI API key. Please check your .env file.")
        return "[Translation failed: Invalid API key]"

    except RateLimitError:
        print("API quota exceeded or too many requests.")
        return "[Translation failed: API quota exceeded]"

    except OpenAIError as e:
        print(f"OpenAI API error: {str(e)}")
        return "[Translation failed: API error]"

    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return "[Translation failed: Unexpected error]"
