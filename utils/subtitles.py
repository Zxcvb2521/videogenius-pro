import whisper_timestamped as whisper
import json
import torch

def generate_subtitles(audio_file: str, video_file: str, output_file: str):
    try:
        # Загружаем модель
        model = whisper.load_model("base", device="cpu")
        audio = whisper.load_audio(audio_file)
        result = whisper.transcribe(model, audio, language="ru")

        # Создаем SRT
        srt_path = output_file.replace(".mp4", ".srt")
        with open(srt_path, "w", encoding="utf-8") as srt:
            for i, segment in enumerate(result["segments"], 1):
                start = segment["start"]
                end = segment["end"]
                text = segment["text"].strip()
                srt.write(f"{i}\n")
                srt.write(f"{format_timestamp(start)} --> {format_timestamp(end)}\n")
                srt.write(f"{text}\n\n")

        # Вжигаем субтитры в видео
        subprocess.run([
            "ffmpeg", "-y", "-i", video_file,
            "-vf", f"subtitles={srt_path}:force_style='FontName=Arial,FontSize=24,PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,BorderStyle=3,Outline=1,Shadow=0'",
            "-c:a", "copy", output_file
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        return output_file
    except Exception as e:
        print(f"Ошибка субтитров: {e}")
        return video_file

def format_timestamp(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = seconds % 60
    return f"{hours:02}:{minutes:02}:{secs:06.3f}".replace(".", ",")
