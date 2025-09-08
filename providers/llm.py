from config.settings import Settings

settings = Settings()

def generate_script_with_llm(topic: str, style="нейтральный") -> str:
    try:
        client = settings.get_current_llm_client()
        provider = settings.current["llm_provider"]
        model = settings.current["llm_model"]

        system_prompt = f"Ты — профессиональный сценарист. Стиль: {style}."
        user_prompt = f"""
        Напиши сценарий для короткого видео (1-2 минуты) на тему: "{topic}".
        Раздели на 3-5 сцен. Каждая сцена в формате:

        Сцена [номер]:
        Визуал: [описание изображения или видео для поиска]
        Текст: [текст для озвучки]

        Не добавляй лишнего. Только сцены.
        """

        if provider == "openai":
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7,
                max_tokens=800
            )
            return response.choices[0].message.content.strip()

        elif provider == "anthropic":
            response = client.messages.create(
                model=model,
                system=system_prompt,
                messages=[{"role": "user", "content": user_prompt}],
                max_tokens=800,
                temperature=0.7
            )
            return response.content[0].text

        elif provider == "mistral":
            response = client.chat.complete(
                model=model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7,
                max_tokens=800
            )
            return response.choices[0].message.content

    except Exception as e:
        return f"Ошибка генерации сценария: {str(e)}"
