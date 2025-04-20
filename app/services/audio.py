import uuid
import os
from gtts import gTTS
import time

# Ensure audio directory exists
AUDIO_DIR = "app/static/audio"
os.makedirs(AUDIO_DIR, exist_ok=True)


async def text_to_speech(text: str, lang: str) -> str:
    # Generate a unique filename for the audio
    start_time = time.time()
    audio_filename = f"{uuid.uuid4()}.mp3"
    audio_path = os.path.join(AUDIO_DIR, audio_filename)
    print(f"Generating audio at: {audio_path}")
    try:
        tts = gTTS(text=text, lang=lang, slow=False)
        tts.save(audio_path)
        if os.path.exists(audio_path):
            print(f"Audio file created successfully: {audio_path}")
        else:
            print(f"Failed to create audio file: {audio_path}")
            return None
        duration = time.time() - start_time
        print(f"Audio generation took {duration:.2f} seconds.")
        return f"static/audio/{audio_filename}"  # Updated URL
    except Exception as e:
        print(f"Error generating audio: {e}")
        return None
