import os
from dotenv import load_dotenv, set_key

class Settings:
    def __init__(self, env_path=".env"):
        self.env_path = env_path
        load_dotenv(env_path)
        self.providers = {
            "llm": {
                "openai": os.getenv("OPENAI_API_KEY", ""),
                "anthropic": os.getenv("ANTHROPIC_API_KEY", ""),
                "mistral": os.getenv("MISTRAL_API_KEY", ""),
            },
            "tts": {
                "elevenlabs": os.getenv("ELEVENLABS_API_KEY", ""),
                "playht": os.getenv("PLAYHT_API_KEY", ""),
                "playht_user_id": os.getenv("PLAYHT_USER_ID", ""),
            },
            "media": {
                "pexels": os.getenv("PEXELS_API_KEY", ""),
                "unsplash": os.getenv("UNSPLASH_API_KEY", ""),
                "openai": os.getenv("OPENAI_API_KEY", ""),  # для DALL·E
            }
        }
        self.current = {
            "llm_provider": os.getenv("CURRENT_LLM_PROVIDER", "openai"),
            "llm_model": os.getenv("CURRENT_LLM_MODEL", "gpt-4-turbo"),
            "tts_provider": os.getenv("CURRENT_TTS_PROVIDER", "elevenlabs"),
            "tts_voice": os.getenv("CURRENT_TTS_VOICE", "Bella"),
            "media_provider": os.getenv("CURRENT_MEDIA_PROVIDER", "pexels"),
        }

    def save_provider_key(self, provider_type, provider_name, key):
        key_name = f"{provider_name.upper()}_API_KEY"
        if provider_name == "playht":
            if "_USER_ID" in key_name:
                key_name = "PLAYHT_USER_ID"
            else:
                key_name = "PLAYHT_API_KEY"
        set_key(self.env_path, key_name, key)
        self.providers[provider_type][provider_name] = key

    def save_current_setting(self, setting_name, value):
        set_key(self.env_path, f"CURRENT_{setting_name.upper()}", value)
        self.current[setting_name] = value

    def get_current_llm_client(self):
        provider = self.current["llm_provider"]
        key = self.providers["llm"][provider]
        if provider == "openai":
            import openai
            return openai.OpenAI(api_key=key)
        elif provider == "anthropic":
            from anthropic import Anthropic
            return Anthropic(api_key=key)
        elif provider == "mistral":
            from mistralai import Mistral
            return Mistral(api_key=key)
        return None

    def get_current_tts_client(self):
        provider = self.current["tts_provider"]
        if provider == "elevenlabs":
            from elevenlabs.client import ElevenLabs
            return ElevenLabs(api_key=self.providers["tts"]["elevenlabs"])
        elif provider == "playht":
            from playht import Client
            return Client(
                user_id=self.providers["tts"]["playht_user_id"],
                api_key=self.providers["tts"]["playht"]
            )
        return None
