import requests
import os
import subprocess
from config.settings import Settings

settings = Settings()

def search_or_generate_visual(query: str, duration=5) -> str:
    provider = settings.current["media_provider"]
    key = settings.providers["media"][provider]

    if provider == "pexels":
        return search_pexels_video(query, key, duration)
    elif provider == "unsplash":
        return search_unsplash_image(query, key, duration)
    elif provider == "openai":
        return generate_dalle_image(query, key, duration)
    else:
        return "videos/fallback.mp4"

def search_pexels_video(query: str, api_key: str, duration=5) -> str:
    try:
        url = "https://api.pexels.com/videos/search"
        headers = {"Authorization": api_key}
        params = {"query": query, "per_page": 1, "orientation": "landscape"}
        response = requests.get(url, headers=headers, params=params).json()

        if not response.get('videos'):
            return "videos/fallback.mp4"

        video_files = response['videos'][0]['video_files']
        hd_video = next((v for v in video_files if v['quality'] == 'hd'), video_files[0])
        video_url = hd_video['link']

        filename = f"videos/clip_{hash(query) % 10000}.mp4"
        with open(filename, 'wb') as f:
            f.write(requests.get(video_url).content)

        output_file = filename.replace(".mp4", "_cut.mp4")
        subprocess.run([
            "ffmpeg", "-y", "-i", filename,
            "-t", str(duration),
            "-c", "copy", output_file
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        return output_file
    except:
        return "videos/fallback.mp4"

def search_unsplash_image(query: str, api_key: str, duration=5) -> str:
    try:
        url = "https://api.unsplash.com/photos/random"
        headers = {"Authorization": f"Client-ID {api_key}"}
        params = {"query": query, "orientation": "landscape"}
        response = requests.get(url, headers=headers, params=params).json()

        image_url = response['urls']['regular']
        image_path = f"videos/image_{hash(query) % 10000}.jpg"
        with open(image_path, 'wb') as f:
            f.write(requests.get(image_url).content)

        # Конвертируем изображение в видео
        video_path = image_path.replace(".jpg", ".mp4")
        subprocess.run([
            "ffmpeg", "-y", "-loop", "1", "-i", image_path,
            "-c:v", "libx264", "-t", str(duration), "-pix_fmt", "yuv420p",
            video_path
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        return video_path
    except:
        return "videos/fallback.mp4"

def generate_dalle_image(query: str, api_key: str, duration=5) -> str:
    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key)

        response = client.images.generate(
            model="dall-e-3",
            prompt=f"Иллюстрация к теме: {query}. Стиль: цифровая живопись.",
            size="1792x1024",
            quality="standard",
            n=1,
        )

        image_url = response.data[0].url
        image_path = f"videos/dalle_{hash(query) % 10000}.jpg"
        with open(image_path, 'wb') as f:
            f.write(requests.get(image_url).content)

        # Конвертируем в видео
        video_path = image_path.replace(".jpg", ".mp4")
        subprocess.run([
            "ffmpeg", "-y", "-loop", "1", "-i", image_path,
            "-c:v", "libx264", "-t", str(duration), "-pix_fmt", "yuv420p",
            video_path
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        return video_path
    except:
        return "videos/fallback.mp4"
