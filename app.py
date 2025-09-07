import os
import gradio as gr
import subprocess
import tempfile
from providers.llm import generate_script_with_llm
from providers.tts import generate_voice
from providers.media import search_or_generate_visual
from utils.subtitles import generate_subtitles
from utils.history import save_history_entry, load_history
from config.settings import Settings

# Инициализация
settings = Settings()
os.makedirs("videos", exist_ok=True)

# Создаём silence.mp3
if not os.path.exists("videos/silence.mp3"):
    import wave
    with wave.open("videos/silence.mp3", "w") as f:
        f.setnchannels(1)
        f.setsampwidth(2)
        f.setframerate(44100)
        f.writeframes(b"\x00\x00" * 44100)

# === Основная логика ===

def create_video_pipeline(topic: str, style: str, add_subtitles: bool, progress=gr.Progress()):
    if not topic.strip():
        return "Введите тему!", None

    progress(0.1, desc="Генерирую сценарий...")
    script = generate_script_with_llm(topic, style)
    if "Ошибка" in script:
        return script, None

    progress(0.3, desc="Создаю аудио и визуал...")
    scenes = parse_script(script)
    if not scenes:
        return "Не удалось распарсить сценарий", None

    video_files = []
    for i, scene in enumerate(progress.tqdm(scenes, desc="Обрабатываю сцены")):
        visual_desc = scene.get("visual", "абстрактный фон")
        voice_text = scene.get("text", "")

        # Медиа
        video_file = search_or_generate_visual(visual_desc, duration=5)
        # Аудио
        audio_file = f"videos/voice_{i}.mp3"
        generate_voice(voice_text, audio_file)

        # Склейка
        temp_video = f"videos/temp_{i}.mp4"
        subprocess.run([
            "ffmpeg", "-y", "-i", video_file, "-i", audio_file,
            "-c:v", "copy", "-c:a", "aac", "-shortest", temp_video
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        video_files.append(temp_video)

    progress(0.8, desc="Склеиваю видео...")
    if len(video_files) == 1:
        final_path = f"videos/{topic.replace(' ', '_')}.mp4"
        os.rename(video_files[0], final_path)
    else:
        list_file = "videos/filelist.txt"
        with open(list_file, "w") as f:
            for vf in video_files:
                f.write(f"file '{os.path.abspath(vf)}'\n")
        final_path = f"videos/{topic.replace(' ', '_')}.mp4"
        subprocess.run([
            "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", list_file,
            "-c", "copy", final_path
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # Субтитры
    if add_subtitles and len(video_files) > 0:
        progress(0.9, desc="Добавляю субтитры...")
        audio_file = f"videos/voice_0.mp3"
        final_path = generate_subtitles(audio_file, final_path, final_path)

    # История
    save_history_entry(topic, final_path)

    progress(1.0, desc="Готово!")
    return "✅ Видео готово!", final_path

def parse_script(script: str) -> list:
    scenes = []
    lines = script.split('\n')
    current_scene = {}
    for line in lines:
        line = line.strip()
        if line.startswith("Сцена") and current_scene:
            scenes.append(current_scene)
            current_scene = {}
        elif "Визуал:" in line:
            current_scene["visual"] = line.replace("Визуал:", "").strip()
        elif "Текст:" in line:
            current_scene["text"] = line.replace("Текст:", "").strip()
    if current_scene:
        scenes.append(current_scene)
    return [s for s in scenes if s.get("visual") and s.get("text")]

# === Gradio UI ===

with gr.Blocks(title="VideoGenius PRO") as demo:
    gr.Markdown("# 🎬 VideoGenius PRO\n### AI-генератор видео с поддержкой множества провайдеров")

    with gr.Tab("Создать видео"):
        topic = gr.Textbox(label="Тема видео", placeholder="Как работает фотосинтез?")
        style = gr.Dropdown(
            label="Стиль изложения",
            choices=["нейтральный", "научный", "развлекательный", "детский", "драматичный"],
            value="нейтральный"
        )
        add_subtitles = gr.Checkbox(label="Добавить субтитры", value=True)
        btn = gr.Button("Создать видео 🚀", variant="primary")
        status = gr.Textbox(label="Статус")
        video = gr.Video(label="Результат")
        btn.click(create_video_pipeline, [topic, style, add_subtitles], [status, video])

    with gr.Tab("История"):
        def load_history_ui():
            history = load_history()
            return "\n".join([
                f"{h['id']}. {h['topic']} ({h['created_at'][:10]}) - {h['status']}"
                for h in history[-10:]
            ])
        history_display = gr.Textbox(label="Последние 10 генераций", lines=10)
        refresh_btn = gr.Button("Обновить историю")
        refresh_btn.click(load_history_ui, None, history_display)

    with gr.Tab("Настройки"):
        gr.Markdown("## 🔌 Настройка API-провайдеров")

        with gr.Tab("LLM (Текст)"):
            llm_provider = gr.Radio(
                ["openai", "anthropic", "mistral"],
                label="Провайдер",
                value=settings.current["llm_provider"]
            )
            openai_key = gr.Textbox(label="OpenAI API Key", type="password", value=settings.providers["llm"]["openai"])
            anthropic_key = gr.Textbox(label="Anthropic API Key", type="password", value=settings.providers["llm"]["anthropic"])
            mistral_key = gr.Textbox(label="Mistral API Key", type="password", value=settings.providers["llm"]["mistral"])
            llm_model = gr.Textbox(label="Модель", value=settings.current["llm_model"])
            save_llm = gr.Button("Сохранить LLM настройки")
            save_llm.click(
                lambda p, o, a, m, mdl: [
                    settings.save_provider_key("llm", "openai", o),
                    settings.save_provider_key("llm", "anthropic", a),
                    settings.save_provider_key("llm", "mistral", m),
                    settings.save_current_setting("llm_provider", p),
                    settings.save_current_setting("llm_model", mdl),
                    "✅ LLM настройки сохранены"
                ][-1],
                [llm_provider, openai_key, anthropic_key, mistral_key, llm_model],
                gr.Textbox()
            )

        with gr.Tab("TTS (Озвучка)"):
            tts_provider = gr.Radio(["elevenlabs", "playht"], label="Провайдер", value=settings.current["tts_provider"])
            elevenlabs_key = gr.Textbox(label="ElevenLabs API Key", type="password", value=settings.providers["tts"]["elevenlabs"])
            playht_key = gr.Textbox(label="PlayHT API Key", type="password", value=settings.providers["tts"]["playht"])
            playht_user_id = gr.Textbox(label="PlayHT User ID", type="password", value=settings.providers["tts"]["playht_user_id"])
            tts_voice = gr.Textbox(label="Голос (ID или имя)", value=settings.current["tts_voice"])
            save_tts = gr.Button("Сохранить TTS настройки")
            save_tts.click(
                lambda p, e, ph, uid, v: [
                    settings.save_provider_key("tts", "elevenlabs", e),
                    settings.save_provider_key("tts", "playht", ph),
                    settings.save_provider_key("tts", "playht", uid) if uid else None,
                    settings.save_current_setting("tts_provider", p),
                    settings.save_current_setting("tts_voice", v),
                    "✅ TTS настройки сохранены"
                ][-1],
                [tts_provider, elevenlabs_key, playht_key, playht_user_id, tts_voice],
                gr.Textbox()
            )

        with gr.Tab("Медиа (Видео/Изображения)"):
            media_provider = gr.Radio(["pexels", "unsplash", "openai"], label="Провайдер", value=settings.current["media_provider"])
            pexels_key = gr.Textbox(label="Pexels API Key", type="password", value=settings.providers["media"]["pexels"])
            unsplash_key = gr.Textbox(label="Unsplash Access Key", type="password", value=settings.providers["media"]["unsplash"])
            dalle_key = gr.Textbox(label="OpenAI API Key (для DALL·E)", type="password", value=settings.providers["media"]["openai"])
            save_media = gr.Button("Сохранить медиа-настройки")
            save_media.click(
                lambda p, px, us, d: [
                    settings.save_provider_key("media", "pexels", px),
                    settings.save_provider_key("media", "unsplash", us),
                    settings.save_provider_key("media", "openai", d),
                    settings.save_current_setting("media_provider", p),
                    "✅ Медиа-настройки сохранены"
                ][-1],
                [media_provider, pexels_key, unsplash_key, dalle_key],
                gr.Textbox()
            )

demo.launch(server_name="0.0.0.0", server_port=7860, share=True)