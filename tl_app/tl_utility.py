import requests
from django.conf import settings
from django.contrib import messages
from django.shortcuts import render
import requests
import json


# tl_utility.py
import requests
from django.conf import settings
import logging

logger = logging.getLogger(__name__) # Use a logger
def check_chat_id(phno):
    TELEGRAM_BOT_TOKEN = settings.TELEGRAM_BOT_TOKEN# Ensure this is correct
    get_updates_url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getUpdates'

    params = {
        'offset': -1,
        'limit': 10
    }

    try:
        logger.info(f"Making request to Telegram getUpdates: {get_updates_url}")
        response = requests.get(get_updates_url, params=params)
        logger.info(f"Telegram getUpdates response status: {response.status_code}")

        result = response.json()
        logger.debug(f"Telegram getUpdates response body: {result}") # Use debug level

        if response.status_code == 200 and result.get("ok"):
            updates = result.get("result", [])
            logger.info(f"Received {len(updates)} Telegram updates.")

            for update in updates:
                message = update.get("message", {})
                chat = message.get("chat", {})
                chat_id = chat.get("id")
                message_text = message.get('text', '')

                logger.info(f"Processing update: chat_id={chat_id}, message_text='{message_text}'")

                if message_text == phno:
                    logger.info(f"Phone number match found! chat_id: {chat_id}")
                    return {'status': True, 'chat_id': chat_id}

            logger.warning("No matching phone number found in recent updates.")
            return {'status': False, 'chat_id': None}
        else:
            logger.error(f"Failed to get updates from Telegram. Status: {response.status_code}, Response: {result.get('description', 'Unknown error')}")
            return {'status': False, 'chat_id': None}

    except requests.exceptions.RequestException as e: # Catch specific requests errors
        logger.error(f"Network or API error during Telegram getUpdates: {e}", exc_info=True)
        return {'status': False, 'chat_id': None}
    except json.JSONDecodeError as e: # Catch JSON parsing errors
         logger.error(f"JSON decode error from Telegram getUpdates response: {e}", exc_info=True)
         return {'status': False, 'chat_id': None}
    except Exception as e: # Catch any other unexpected errors
        logger.error(f"Unexpected Exception during Telegram getUpdates: {e}", exc_info=True)
        return {'status': False, 'chat_id': None}

# Ensure send_file_to_telegram in tl_utility.py also uses detailed logging in its except block
# ... (rest of tl_utility.py)


def send_file_to_telegram(file_obj,filename, message,token):

    #print(file_obj)
    print("bot token :",settings.TELEGRAM_BOT_TOKEN)
    print("chat id :",token)

    TELEGRAM_BOT_TOKEN=settings.TELEGRAM_BOT_TOKEN
    file_type='Photo' if file_obj in ['.jpg', '.jpeg','.svg' ,'.png', '.gif', '.bmp','.webp'] else 'Document'

    url=f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/send{file_type}'

    data={
        'chat_id':token,
        'caption':message
    }

    files={
        f"{file_type.lower()}":(filename,file_obj)
    }

    try:  # Debugging
        response = requests.post(url, data=data, files=files)
        return response.json()
    except Exception as e:
        print(f"Error uploading {filename}: {e}")
        return {"ok": False, "error": str(e)}

    




def fetch_file_from_telegram(file_id):
    # Step 1: Get the file path from Telegram
    url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN1}/getFile"
    response = requests.get(url, params={'file_id': file_id})
    file_info = response.json()

    if file_info['ok']:
        file_path = file_info['result']['file_path']

        # Step 2: Download the file using the file path
        file_url = f"https://api.telegram.org/file/bot{settings.TELEGRAM_BOT_TOKEN1}/{file_path}"
        file_response = requests.get(file_url)

        # You can now use file_response.content to access the file data
        #print("successs")
        return file_response.content
    else:
        raise Exception("Failed to fetch file from Telegram")



def get_last_5_photos():
    url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/getUpdates"
    response = requests.get(url)
    updates = response.json()

    if not updates.get('ok'):
        raise Exception("Failed to fetch updates from Telegram")

    photo_file_ids = []

    # Iterate through the updates to find photo messages
    for update in updates.get('result', []):
        message = update.get('message', {})
        if 'photo' in message:
            # Get the highest resolution photo
            photo = message['photo'][-1]
            photo_file_ids.append(photo['file_id'])

    # Log the photo file IDs
    #print("Photo file IDs:", photo_file_ids)

    # Return the last 5 photo file IDs
    return photo_file_ids[-5:]

def fetch_photo_from_telegram(file_id):
    try:
        print(f"Starting fetch_photo_from_telegram with file_id: {file_id}")  # Debug log
        
        url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/getFile"
        print(f"Making request to URL: {url}")  # Debug log
        
        response = requests.get(url, params={'file_id': file_id})
        file_info = response.json()
        print(f"File info response for {file_id}:", file_info)  # Debug log

        if file_info.get('ok'):
            file_path = file_info['result']['file_path']
            file_url = f"https://api.telegram.org/file/bot{settings.TELEGRAM_BOT_TOKEN}/{file_path}"
            print(f"Downloading file from: {file_url}")  # Debug log
            
            file_response = requests.get(file_url)
            print(f"Download status code: {file_response.status_code}")  # Debug log
            
            return file_response.content
        else:
            print(f"Error in file info response: {file_info}")  # Debug log
            raise Exception(f"Failed to fetch file from Telegram: {file_info.get('description', 'Unknown error')}")
    except Exception as e:
        print(f"Exception in fetch_photo_from_telegram: {str(e)}")  # Debug log
        raise
