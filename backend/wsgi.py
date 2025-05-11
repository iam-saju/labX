import os
import logging

from django.core.wsgi import get_wsgi_application

# Add logging here
logging.basicConfig(level=logging.INFO)
logging.info("WSGI application loading...")

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

try:
    application = get_wsgi_application()
    logging.info("WSGI application loaded successfully.")
except Exception as e:
    logging.error("Error loading WSGI application:", exc_info=True) # Log the traceback
    raise # Re-raise the exception so Railway sees the failure