import uuid
import os
from gtts import gTTS
import time
import vercel_blob


async def text_to_speech(text: str, lang: str) -> str:
    # Generate a unique filename for the audio
    start_time = time.time()
    audio_filename = f"{uuid.uuid4()}.mp3"
    temp_path = os.path.join("/tmp", audio_filename)  # Use /tmp for Vercel
    print(f"Generating audio at: {temp_path}")
    try:
        tts = gTTS(text=text, lang=lang, slow=False)
        tts.save(temp_path)
        with open(temp_path, "rb") as f:
            audio_data = f.read()
        # Upload to Vercel Blob
        blob = vercel_blob.put(
            f"audio/{audio_filename}", audio_data, {"access": "public"})
        os.remove(temp_path)  # Clean up
        return blob["url"]
    except Exception as e:
        print(f"Error generating audio: {e}")
        return None
