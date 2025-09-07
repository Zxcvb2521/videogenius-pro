import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler
from dotenv import load_dotenv
from app import generate_video_pipeline  # Импортируем основную логику
import asyncio

# Загружаем переменные окружения
load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
if not TELEGRAM_TOKEN:
    raise ValueError("TELEGRAM_TOKEN не установлен в .env")

# Логирование
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Хранилище задач (в памяти, для MVP)
user_tasks = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎬 Привет! Я VideoGenius AI Agent.\n\n"
        "Отправь мне тему — я создам видео и загружу его на YouTube!"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    topic = update.message.text
    user_id = update.message.from_user.id

    # Показываем клавиатуру с выбором: только видео / видео + YouTube
    keyboard = [
        [
            InlineKeyboardButton("🎥 Только видео", callback_data=f"video_only|{topic}"),
            InlineKeyboardButton("📺 Загрузить на YouTube", callback_data=f"youtube|{topic}")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        f'Тема: "{topic}"\nВыбери действие:',
        reply_markup=reply_markup
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data.split("|")
    action = data[0]
    topic = data[1]
    user_id = query.from_user.id

    await query.edit_message_text(text=f"⏳ Начинаю создание видео по теме:\n\n«{topic}»...")

    # Запускаем генерацию видео
    try:
        status = ""
        video_path = None
        async for status, video_path in generate_video_pipeline(topic, "нейтральный", True):
            if video_path:
                break
            else:
                await query.edit_message_text(text=status)

        if not video_path or not os.path.exists(video_path):
            await query.edit_message_text(text="❌ Ошибка: не удалось создать видео.")
            return

        # Если выбрано "Только видео"
        if action == "video_only":
            await context.bot.send_video(
                chat_id=query.message.chat_id,
                video=open(video_path, 'rb'),
                caption=f"✅ Видео по теме «{topic}» готово!"
            )
            await query.edit_message_text(text="Видео отправлено!")

        # Если выбрано "Загрузить на YouTube"
        elif action == "youtube":
            await query.edit_message_text(text="📤 Загружаю видео на YouTube...")
            try:
                youtube_url = upload_to_youtube(video_path, topic)
                await context.bot.send_message(
                    chat_id=query.message.chat_id,
                    text=f"✅ Видео по теме «{topic}» загружено на YouTube!\n\n{youtube_url}"
                )
            except Exception as e:
                await context.bot.send_message(
                    chat_id=query.message.chat_id,
                    text=f"⚠️ Видео создано, но не удалось загрузить на YouTube:\n{str(e)}"
                )
                await context.bot.send_video(
                    chat_id=query.message.chat_id,
                    video=open(video_path, 'rb'),
                    caption="🎥 Вот ваше видео:"
                )

    except Exception as e:
        logger.error(f"Ошибка при генерации видео: {e}")
        await query.edit_message_text(text=f"❌ Ошибка: {str(e)}")

def upload_to_youtube(video_path: str, title: str) -> str:
    """Загружает видео на YouTube и возвращает URL"""
    from googleapiclient.discovery import build
    from googleapiclient.http import MediaFileUpload
    from google.oauth2.credentials import Credentials

    # Настройки YouTube API
    SCOPES = ['https://www.googleapis.com/auth/youtube.upload']
    API_SERVICE_NAME = 'youtube'
    API_VERSION = 'v3'
    CLIENT_SECRETS_FILE = 'client_secret.json'  # Должен быть в корне проекта
    TOKEN_FILE = 'token.json'

    creds = None
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

    if not creds:
        raise Exception("YouTube API не настроен. См. инструкцию.")

    youtube = build(API_SERVICE_NAME, API_VERSION, credentials=creds)

    request_body = {
        'snippet': {
            'title': title[:100],
            'description': f'Видео создано AI по теме: {title}',
            'tags': ['AI', 'VideoGenius', 'автоматизация'],
            'categoryId': '27'  # Образование
        },
        'status': {
            'privacyStatus': 'public',  # или 'private', 'unlisted'
            'selfDeclaredMadeForKids': False
        }
    }

    media = MediaFileUpload(video_path, chunksize=-1, resumable=True)
    request = youtube.videos().insert(
        part="snippet,status",
        body=request_body,
        media_body=media
    )

    response = None
    while response is None:
        status, response = request.next_chunk()

    video_id = response['id']
    return f"https://youtu.be/{video_id}"

def main():
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_handler(CallbackQueryHandler(button_handler))

    logger.info("Telegram-бот запущен...")
    application.run_polling()

if __name__ == '__main__':
    main()