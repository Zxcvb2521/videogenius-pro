import json
import os
from datetime import datetime

HISTORY_FILE = "videos/history.json"

def load_history():
    if not os.path.exists(HISTORY_FILE):
        return []
    with open(HISTORY_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_history_entry(topic, video_path, status="success"):
    history = load_history()
    entry = {
        "id": len(history) + 1,
        "topic": topic,
        "video_path": video_path,
        "status": status,
        "created_at": datetime.now().isoformat(),
        "settings": {
            "llm_provider": os.getenv("CURRENT_LLM_PROVIDER", "openai"),
            "tts_provider": os.getenv("CURRENT_TTS_PROVIDER", "elevenlabs"),
            "media_provider": os.getenv("CURRENT_MEDIA_PROVIDER", "pexels"),
        }
    }
    history.append(entry)
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)
    return entry
