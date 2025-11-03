import os
import asyncio
from pydub import AudioSegment
from telegram import Update
from telegram.ext import Application, MessageHandler, CommandHandler, ContextTypes, filters

TOKEN = "123716274:AAHrGxV9fOj1N4aOI0Ogj-sXGJyMB4o6wGk"

async def voice_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file = await update.message.voice.get_file()
    ogg_path = "voice.ogg"
    mp3_path = "voice.mp3"

    await file.download_to_drive(ogg_path)

    sound = AudioSegment.from_file(ogg_path, format="ogg")
    sound.export(mp3_path, format="mp3")

    await update.message.reply_document(open(mp3_path, "rb"))

    os.remove(ogg_path)
    os.remove(mp3_path)



async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("ГС в MP3.\nОтправь мне voice-сообщение!")


async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"Ты написал: {update.message.text}")


async def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start_handler))  # команда /start
    app.add_handler(MessageHandler(filters.VOICE, voice_handler))  # голосовые
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler))  # текст

    print("🤖 Бот запущен...")

    await app.initialize()
    await app.start()
    await app.updater.start_polling()

    await asyncio.Event().wait()


if __name__ == "__main__":
    asyncio.run(main())
