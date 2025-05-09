# bot/apps.py
from django.apps import AppConfig
import threading

class BotConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'bot'

    def ready(self):
        from .bot import start_bot
        thread = threading.Thread(target=start_bot)
        thread.start()
