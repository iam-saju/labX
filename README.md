Qubit
Turn Telegram into cloud storage for your files
What is Qubit?
Qubit lets you use Telegram to store and manage your files. Upload, find, and share files easily through Telegram.
Main Features

Store unlimited files using Telegram
Keep your files secure with Telegram's encryption
Organize files in folders
Search for files by name or type
Works on all devices with Telegram
Preview files before downloading

Requirements

Python 3.8+
Telegram account
Telegram API key and hash

Dependencies

Django 5.2+
python-telegram-bot
requests
pillow
python-dotenv
psycopg2-binary (for PostgreSQL)
celery (for background tasks)
redis (for caching)
telethon

Setup
bash# Get the code
git clone https://github.com/yourusername/qubit.git
cd qubit

# Install required packages
pip install -r requirements.txt

# Set up your config
cp .env.example .env
# Edit .env with your Telegram API details
How to Use

Start the server: python manage.py runserver
Open in browser: http://127.0.0.1:8000/
Log in with your Telegram account
Upload and manage your files

Security

Files are stored in your Telegram account, not our servers
Uses Telegram's built-in security

License
MIT License
