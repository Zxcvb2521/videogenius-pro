# videogenius-pro
VideoGenius PRO — это AI-агент, который автоматически создаёт короткие видео (1–3 минуты) на основе текстовой темы. 
AI-агент для генерации видео по текстовой теме с поддержкой множества API, Telegram-бота и YouTube API.
Проект поддерживает:

🧠 Генерацию сценария через LLM (OpenAI, Anthropic, Mistral)
🔊 Озвучку через TTS (ElevenLabs, PlayHT)
🖼️ Подбор или генерацию визуального ряда (Pexels, Unsplash, DALL·E)
📜 Автоматическую генерацию субтитров
🤖 Интерфейс через Telegram-бота
📺 Автоматическую загрузку на YouTube
🖥️ Веб-интерфейс на Gradio
🐳 Запуск в Docker

🗂️ Структура проекта
VideoGenius PRO/
├── app.py                          # Основной веб-интерфейс (Gradio)
├── telegram_bot.py                 # Telegram-бот для генерации и загрузки видео
├── Dockerfile                      # Конфигурация Docker-образа
├── requirements.txt                # Зависимости Python
├── .env                            # API-ключи (не коммитить!)
├── .env.example                    # Шаблон .env
├── .dockerignore                   # Игнор файлов при сборке
├── start_videogenius.bat           # Ярлык для запуска веб-интерфейса
├── start_telegram.bat              # Ярлык для запуска Telegram-бота
├── client_secret.json              # Конфиг YouTube API (скачивается из Google Cloud)
├── token.json                      # Токен доступа YouTube API (генерируется при авторизации)
├── playht-sdk/                     # Локальная копия PlayHT SDK (скачивается при установке)
│   └── src/
├── videos/                         # Папка для сохранения сгенерированных видео (создаётся автоматически)
├── providers/                      # Модули для работы с API
│   ├── __init__.py
│   ├── llm.py                      # Работа с LLM (OpenAI, Anthropic, Mistral)
│   ├── tts.py                      # Работа с TTS (ElevenLabs, PlayHT)
│   └── media.py                    # Работа с медиа (Pexels, Unsplash, DALL·E)
├── utils/                          # Вспомогательные утилиты
│   ├── __init__.py
│   ├── history.py                  # История генераций
│   └── subtitles.py                # Генерация и вжигание субтитров
└── config/
    └── settings.py                 # Управление настройками и API-ключами

📄 Описание ключевых файлов
app.py
Основной файл веб-приложения на Gradio.
Содержит:

Интерфейс с вкладками: «Создать видео», «История», «Настройки»
Пайплайн генерации видео: тема → сценарий → аудио → визуал → монтаж → субтитры
Интеграцию с модулями из providers/ и utils/
telegram_bot.py
Telegram-бот на python-telegram-bot.

Позволяет:
Отправлять тему для генерации видео
Выбирать: получить видео в чате или загрузить на YouTube
Получать ссылку на видео после загрузки

Dockerfile
Сборка образа на python:3.11.
Устанавливает:
ffmpeg, git, системные зависимости
Все Python-зависимости из requirements.txt
PlayHT SDK из локальной папки playht-sdk/src
Не копирует client_secret.json и token.json — они монтируются при запуске

requirements.txt
Список всех зависимостей:
txt
gradio==4.29.0
openai>=1.0.0
anthropic>=0.25.0
mistralai>=0.3.0
requests>=2.31.0
python-dotenv>=1.0.1
elevenlabs>=1.0.0,<2.0.0
python-telegram-bot>=20.0
google-api-python-client>=2.0
google-auth>=2.0
google-auth-oauthlib>=0.4
google-auth-httplib2>=0.1
imageio>=2.31.0
imageio-ffmpeg>=0.4.9
ffmpeg-python>=0.2.0
numpy>=1.24.0
whisper-timestamped>=1.14.4
torch>=2.0.0
transformers>=4.36.0
pillow>=10.0.0
config/settings.py
Централизованное управление настройками:

Загрузка и сохранение API-ключей в .env
Хранение текущих настроек (провайдеры, модели, голоса)
Получение клиентов для текущих провайдеров
providers/
Модули для работы с внешними API:

llm.py — генерация сценария
tts.py — генерация аудио
media.py — поиск/генерация видео и изображений
utils/
Вспомогательные функции:

history.py — сохранение истории генераций в videos/history.json
subtitles.py — генерация субтитров через whisper-timestamped и вжигание в видео через ffmpeg
.env.example

Шаблон для настройки API-ключей:
# LLM
OPENAI_API_KEY=
ANTHROPIC_API_KEY=
MISTRAL_API_KEY=

# TTS
ELEVENLABS_API_KEY=
PLAYHT_API_KEY=
PLAYHT_USER_ID=

# Медиа
PEXELS_API_KEY=
UNSPLASH_API_KEY=

# Telegram
TELEGRAM_TOKEN=

# Текущие настройки
CURRENT_LLM_PROVIDER=openai
CURRENT_LLM_MODEL=gpt-4-turbo
CURRENT_TTS_PROVIDER=elevenlabs
CURRENT_TTS_VOICE=Bella
CURRENT_MEDIA_PROVIDER=pexels

.dockerignore
Игнорирует отсутствующие файлы при сборке:
client_secret.json
token.json

start_videogenius.bat
Ярлык для запуска веб-интерфейса:
@echo off
cd /d "C:\Users\...\...\VideoGenius AI Agent\VideoGenius PRO"
docker run -it --rm -p 7860:7860 --env-file .env videogenius-pro
pause

start_telegram.bat
Ярлык для запуска Telegram-бота:
@echo off
cd /d "C:\Users\...\...\VideoGenius AI Agent\VideoGenius PRO"
python telegram_bot.py
pause

🛠️ Инструкция по установке и запуску
Шаг 1: Подготовка окружения
Установи Docker Desktop: https://www.docker.com/products/docker-desktop
Создай папку проекта:

C:\Users\...\...\VideoGenius AI Agent\VideoGenius PRO\
Распакуй все файлы проекта в эту папку.

Шаг 2: Настройка API-ключей
Переименуй .env.example в .env
Заполни API-ключи (можно оставить пустыми — тогда соответствующие функции не будут работать):
OpenAI: https://platform.openai.com/api-keys
ElevenLabs: https://elevenlabs.io
Pexels: https://www.pexels.com/api/
Telegram Bot: через @BotFather
YouTube API: см. ниже

Шаг 3: Сборка Docker-образа
powershell
cd "C:\Users\...\...\VideoGenius AI Agent\VideoGenius PRO"
docker build --no-cache -t videogenius-pro .

Шаг 4: Запуск веб-интерфейса
Дважды кликни по start_videogenius.bat → открой публичную ссылку https://xxxx.gradio.app

Шаг 5: Запуск Telegram-бота
Убедись, что TELEGRAM_TOKEN заполнен в .env
Дважды кликни по start_telegram.bat
Найди своего бота в Telegram → отправь /start
Шаг 6: Настройка YouTube API (опционально)
Перейди в Google Cloud Console
Создай проект → включи YouTube Data API v3
Создай OAuth 2.0 Client ID → скачай JSON → переименуй в client_secret.json → положи в корень проекта
Запусти Telegram-бота локально (не в Docker):

powershell
python telegram_bot.py

Следуй инструкциям в консоли → авторизуйся → token.json создастся автоматически

Теперь можно запускать бота в Docker с монтированием токена:
powershell
docker run -it --rm -p 7860:7860 --env-file .env ^
  -v "C:\Users\...\...\VideoGenius AI Agent\VideoGenius PRO\client_secret.json:/app/client_secret.json" ^
  -v "C:\Users\...\...\VideoGenius AI Agent\VideoGenius PRO\token.json:/app/token.json" ^
  videogenius-pro
  
🚀 Возможности для развития
🌐 Добавление веб-хуков для асинхронной генерации
🗃️ Интеграция с базой данных (PostgreSQL) для хранения истории
☁️ Развёртывание на облачных платформах (Render, Railway, AWS)
🎚️ Добавление настроек качества, разрешения, длительности
🎨 Поддержка шаблонов видео (логотип, заставка, титры)
📊 Аналитика и логирование
💰 Монетизация через API или подписки

    
