# bot/telegram_bot.py
import logging
from telegram.ext import Updater, MessageHandler, Filters
from django.conf import settings
import requests
from .models import TelegramPhoto

BOT_TOKEN = '7232641920:AAHtX-4ND1rarGgzXXvvy7l3FtIbBEsDWq8'

def start_bot():
    updater = Updater(token=BOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    def handle_photo(update, context):
        message = update.message
        photo = message.photo[-1]  # Highest quality version
        caption = message.caption or ""
        file_id = photo.file_id

        # Get Telegram file info and URL
        file_info = context.bot.get_file(file_id)
        file_url = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file_info.file_path}"

        # ✅ Immediately send back the same image as confirmation
        context.bot.send_photo(
            chat_id=message.chat_id,
            photo=file_id,
            caption=f"✅ Received your photo!\nTag: {caption}"
        )

        # ✅ Save it to DB
        TelegramPhoto.objects.create(
            file_id=file_id,
            caption=caption,
            file_url=file_url
        )

    dispatcher.add_handler(MessageHandler(Filters.photo, handle_photo))

    updater.start_polling()
