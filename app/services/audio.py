import uuid
import os
from gtts import gTTS


# Ensure audio directory exists
AUDIO_DIR = "app/static/audio"


async def text_to_speech(text: str, lang: str) -> str:
    # Generate a unique filename for the audio
    audio_filename = f"{uuid.uuid4()}.mp3"
    audio_path = os.path.join(AUDIO_DIR, audio_filename)

    # Generate audio using gTTS
    tts = gTTS(text=text, lang=lang, slow=False)
    tts.save(audio_path)

    # Return the URL to access the audio file
    return f"static/audio/{audio_filename}"
