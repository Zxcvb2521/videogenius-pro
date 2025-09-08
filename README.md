**Расширеная версия VideoGenius AI Agent** с:

✅ Страницей настроек API  
✅ Поддержкой нескольких поставщиков (OpenAI, Anthropic, Mistral, ElevenLabs, PlayHT, Pexels, Unsplash, DALL·E и др.)  
✅ Прогресс-баром, историей, субтитрами, экспортом  
✅ Возможностью выбирать модели, голоса, стили

---
## 🚀 VideoGenius PRO 

---
## 📁 Структура проекта
```
videogenius/
├── app.py                  # Основной интерфейс + логика
├── providers/              # Модули поставщиков API
│   ├── llm.py              # OpenAI, Anthropic, Mistral
│   ├── tts.py              # ElevenLabs, PlayHT
│   ├── media.py            # Pexels, Unsplash, DALL·E
│   └── __init__.py
├── utils/
│   ├── history.py          # История генераций
│   ├── subtitles.py        # Генерация субтитров
│   └── __init__.py
├── config/
│   └── settings.py         # Загрузка/сохранение настроек
├── videos/                 # Выходные видео
├── .env
├── Dockerfile
├── requirements.txt
└── README.md
```
---
## 📦 1. Обновлённый `requirements.txt`
---
## 🛠️ 2. `config/settings.py` — управление настройками
---
## 🧠 3. `providers/llm.py` — поддержка нескольких LLM
---
## 🔊 4. `providers/tts.py` — несколько TTS-провайдеров
---
## 🖼️ 5. `providers/media.py` — поиск и генерация медиа
---
## 📜 6. `utils/subtitles.py` — генерация субтитров
---
## 📚 7. `utils/history.py` — история генераций
---
## 🎥 8. Обновлённый `app.py` — финальная версия
---

## 💡 Что теперь умеет VideoGenius PRO:
- ✅ Выбор LLM: OpenAI, Anthropic, Mistral
- ✅ Выбор TTS: ElevenLabs, PlayHT
- ✅ Выбор медиа: Pexels, Unsplash, DALL·E
- ✅ Субтитры через Whisper
- ✅ История генераций
- ✅ Прогресс-бар
- ✅ Настройка стиля изложения
- ✅ Сохранение всех настроек в `.env`
- ✅ Гибкая архитектура для добавления новых провайдеров

---
## 🚀 Как добавить нового провайдера?
1. Добавь ключ в `settings.py`
2. Реализуй функцию в соответствующем модуле (`llm.py`, `tts.py`, `media.py`)
3. Добавь элементы управления в Gradio-интерфейс
4. Обнови логику выбора в основном пайплайне

---
**профессиональный AI-видеогенератор** с поддержкой множества API — готов к использованию, масштабированию и коммерциализации 🚀

---
 Ниже — **полная инструкция по установке и запуску VideoGenius PRO** — AI-агента для генерации видео на основе текстовой темы с поддержкой множества API-провайдеров.

---
# 🚀 VideoGenius PRO — Инструкция по установке и запуску

---
## 📋 Содержание

1. **Системные требования**
2. **Установка через Docker (рекомендуется)**
3. **Локальный запуск (альтернатива)**
4. **Настройка API-ключей**
5. **Использование интерфейса**
6. **Расширение функционала**
7. **Поиск и устранение неисправностей**

---
## 1. 🖥️ Системные требования

- **ОС**: Windows 10/11, macOS, Linux
- **Docker** (рекомендуется) или Python 3.10+
- **RAM**: 4 ГБ+ (8 ГБ рекомендуется)
- **Диск**: 2 ГБ свободного места
- **Интернет**: для загрузки моделей и доступа к API

---
## 2. 🐳 Установка через Docker (рекомендуется)

### Шаг 1: Установка Docker Desktop

- Windows/macOS: [https://www.docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop)
- Linux: `sudo apt install docker.io docker-compose`

> ✅ Проверка установки:  
> ```bash
> docker --version
> ```

---
### Шаг 2: Распакуй архив проекта

Создай папку, например:

```bash
mkdir VideoGenius-PRO && cd VideoGenius-PRO
```

Распакуй туда все файлы из ZIP-архива.

---
### Шаг 3: Создай `.env` файл если отсутствует

```
> 💡 Получи ключи:
> - OpenAI: https://platform.openai.com/api-keys
> - ElevenLabs: https://elevenlabs.io
> - Pexels: https://www.pexels.com/api/
> - Anthropic: https://console.anthropic.com
> - Mistral: https://console.mistral.ai
> - PlayHT: https://play.ht
> - Unsplash: https://unsplash.com/developers


Интеграция YouTube API

📄 1. Настрой YouTube API
Шаг 1: Создай проект в Google Cloud Console
Перейди: https://console.cloud.google.com/
Создай новый проект → назови “VideoGenius YouTube”
Включи API: YouTube Data API v3
Шаг 2: Создай OAuth 2.0 Client ID
Перейди в “Credentials”
Нажми “Create Credentials” → “OAuth client ID”
Выбери “Desktop app”
Скачай JSON → переименуй в client_secret.json → положи в корень проекта
Шаг 2: Получи токен доступа
При первом запуске бота — он попросит авторизоваться.
Следуй ссылке в консоли → войди в Google → разреши доступ → скопируй код → вставь в консоль.

Токен сохранится в token.json.

---
### Шаг 4: Сборка и запуск контейнера

```bash
docker build --no-cache -t videogenius-pro .
docker run -it --rm -p 7860:7860 --env-file .env videogenius-pro
```

---
### Шаг 5: Открой в браузере

После запуска ты увидишь:

```
Running on public URL: https://xxxxx.gradio.app
```

👉 **Открой эту ссылку в браузере** — интерфейс готов к использованию!

---

## 3. 💻 Локальный запуск (без Docker)

### Шаг 1: Установи Python 3.10+

Скачай с [python.org](https://www.python.org/downloads/) и установи.

> ✅ Проверь:  
> ```bash
> python --version
> pip --version
> ```

---
### Шаг 2: Установи зависимости

```bash
pip install -r requirements.txt
```

> ⚠️ Если будут ошибки с `torch` или `ffmpeg` — используй Docker.

---
### Шаг 3: Запусти приложение

```bash
python app.py
```

→ Открой: http://localhost:7860  
→ Или публичную ссылку, если `share=True`

---
## 4. ⚙️ Настройка API-ключей

После первого запуска:

1. Перейди во вкладку **«Настройки»**
2. Заполни API-ключи для нужных провайдеров
3. Нажми «Сохранить»
4. Ключи сохранятся в `.env` файл
5. Перезапусти приложение (если запущено локально)

> ✅ Все ключи хранятся локально — не передаются на сервера.

---

## 5. 🎬 Использование интерфейса

### Вкладка «Создать видео»

- Введи **тему** (например, *“Как работает фотосинтез”*)
- Выбери **стиль** (научный, развлекательный и т.д.)
- Включи/выключи **субтитры**
- Нажми **«Создать видео»**
- Жди 1–3 минуты
- Скачай результат

### Вкладка «История»

- Просматривай последние 10 генераций
- Видишь тему, дату, статус, использованные настройки

### Вкладка «Настройки»

- Настраивай LLM, TTS, медиа-провайдеров
- Меняй текущие модели и голоса
- Проверяй работоспособность ключей

---
## 6. ➕ Расширение функционала

### Добавить нового провайдера

Пример: добавим **Google TTS**

1. Добавь в `.env`:
   ```env
   GOOGLE_TTS_API_KEY=
   ```

2. В `config/settings.py` → `providers["tts"]`:
   ```python
   "google": os.getenv("GOOGLE_TTS_API_KEY", ""),
   ```

3. В `providers/tts.py` → добавь функцию:
   ```python
   elif provider == "google":
       from gtts import gTTS
       tts = gTTS(text=text, lang='ru')
       tts.save(filename)
   ```

4. В `app.py` → добавь в выбор провайдера:
   ```python
   tts_provider = gr.Radio([... "google"], ...)
   ```

---
## 7. 🛠️ Поиск и устранение неисправностей

| Проблема | Решение |
|----------|---------|
| `ModuleNotFoundError` | Убедись, что все зависимости установлены. Используй Docker. |
| `API key not set` | Перейди в «Настройки» → введи ключи → сохрани → перезапусти. |
| Видео не генерируется | Проверь логи в консоли — там будет точная ошибка. |
| Gradio не открывается | Используй `share=True` → открой публичную ссылку. |
| Медленная генерация | Это нормально — загрузка видео + озвучка + монтаж занимает время. |
| Ошибки Whisper | Убедись, что аудиофайл существует и не пустой. |

---

---
## 🚀 Готово!

Ты установил **полностью рабочий AI-видеогенератор** с поддержкой:

- 🧠 OpenAI, Anthropic, Mistral
- 🔊 ElevenLabs, PlayHT
- 🖼️ Pexels, Unsplash, DALL·E
- 📜 Субтитры, история, прогресс-бар

---
 💪🎥
 
 🤖 Telegram Bot API
Отправляй текст — бот предложит выбор:

🎥 Только видео
📺 Загрузить на YouTube
📺 YouTube API
Автоматическая загрузка через google-api-python-client.

Требует:

client_secret.json
token.json
Формат видео: MP4, до 15 минут (ограничение API).

☁️ РАЗВЁРТЫВАНИЕ НА RENDER.COM (БЕСПЛАТНО)
Render.com — лучший выбор для Gradio + Docker — бесплатный тариф, поддержка Docker, HTTPS, автообновление.

Шаг 1: Зарегистрируйся
→ https://render.com

Шаг 2: Создай “Web Service”
Нажми “New +” → “Web Service”
Подключи репозиторий videogenius-pro
Выбери:
Runtime: Docker
Plan: Free
Region: Oregon (или ближе к тебе)
Auto-deploy: Yes

Шаг 3: Добавь переменные окружения
В разделе “Environment” → “Add Environment Variable”:

1. OPENAI_API_KEY = ваш_ключ
2. ELEVENLABS_API_KEY = ваш_ключ
3. PEXELS_API_KEY = ваш_ключ
4. TELEGRAM_TOKEN = ваш_токен
5. CURRENT_LLM_PROVIDER = openai
6. CURRENT_TTS_PROVIDER = elevenlabs
7. CURRENT_MEDIA_PROVIDER = pexels

💡 Render сохранит их безопасно — они не попадут в логи. 

Шаг 4: Деплой
Нажми “Create Web Service” → жди 3–5 минут → получишь URL вида:

https://videogenius-pro.onrender.com

