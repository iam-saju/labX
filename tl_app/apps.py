# tl_app/apps.py
from django.apps import AppConfig
import logging
from django.conf import settings

logger = logging.getLogger(__name__)

class TlAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tl_app'

    def ready(self):
        try:
            logger.info("tl_app AppConfig.ready() is running...")
            # Add any initialization code here that might fail
            # Example: checking for environment variables or external service connectivity
            if not settings.TELEGRAM_BOT_TOKEN1:
                 logger.error("TELEGRAM_BOT_TOKEN1 environment variable is not set!")
                 # Consider raising an exception if the token is critical for startup
                 # raise EnvironmentError("TELEGRAM_BOT_TOKEN1 not configured")

            logger.info("tl_app AppConfig.ready() completed successfully.")
        except Exception as e:
            logger.error(f"Exception caught during tl_app AppConfig.ready(): {e}", exc_info=True)
            # Re-raise the exception to ensure the container crashes and the traceback is logged
            raise