from config.settings import Settings
import os

settings = Settings()

def generate_voice(text: str, filename: str):
    try:
        provider = settings.current["tts_provider"]
        client = settings.get_current_tts_client()

        if provider == "elevenlabs":
            voice = settings.current["tts_voice"]
            audio_generator = client.generate(
                text=text,
                voice=voice,
                model="eleven_multilingual_v2"
            )
            with open(filename, "wb") as f:
                for chunk in audio_generator:
                    if chunk:
                        f.write(chunk)

        elif provider == "playht":
            import io
            voice = settings.current["tts_voice"]
            response = client.tts(
                text=text,
                voice=voice,
                output_format="mp3"
            )
            audio_data = b"".join(chunk for chunk in response)
            with open(filename, "wb") as f:
                f.write(audio_data)

    except Exception as e:
        print(f"Ошибка TTS: {e}")
        # fallback
        with open("videos/silence.mp3", "rb") as src, open(filename, "wb") as dst:
            dst.write(src.read())
