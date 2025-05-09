import requests
from django.conf import settings
from django.contrib import messages
from django.shortcuts import render

import requests

def check_chat_id(phno):
    TELEGRAM_BOT_TOKEN = settings.TELEGRAM_BOT_TOKEN1
    get_updates_url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getUpdates'
    
    # Add offset parameter to get only new updates
    # You can also add a timeout parameter for long polling
    params = {
        'offset': -1,  # This gets the latest update and marks previous ones as read
        'limit': 10    # Limit the number of updates to retrieve
    }
    
    try:
        response = requests.get(get_updates_url, params=params)
        result = response.json()
        
        if response.status_code == 200 and result.get("ok"):
            updates = result.get("result", [])
            
            # Process the latest updates
            for update in updates:
                message = update.get("message", {})
                
                chat = message.get("chat", {})
                chat_id = chat.get("id")
                print(message['text'],"\n")
                
                # Store the update_id for future requests
                latest_update_id = update.get("update_id", 0)
                
                # You could store this chat_id in your database
                print(f"Found chat_id: {chat_id}")
                
                # For testing - if the phone number matches last 4 digits of chat_id
                if message['text'] == phno:
                    return {'status':True,'chat_id':chat_id}
            
            # If we went through all updates and didn't find a match
            return {'status':False,'chat_id':None}
        else:
            print("Failed to get updates:", result.get("description", "Unknown error"))
            return {'status':False,'chat_id':None}
            
    except Exception as e:
        print(f"Exception during updates retrieval: {str(e)}")
        return {'status':False,'chat_id':None}

def send_file_to_telegram(file_obj,filename, message,token):

    #print(file_obj)
    print("bot token :",settings.TELEGRAM_BOT_TOKEN1)
    print("chat id :",token)

    TELEGRAM_BOT_TOKEN=settings.TELEGRAM_BOT_TOKEN1
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
    url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/getFile"
    response = requests.get(url, params={'file_id': file_id})
    file_info = response.json()

    if file_info['ok']:
        file_path = file_info['result']['file_path']

        # Step 2: Download the file using the file path
        file_url = f"https://api.telegram.org/file/bot{settings.TELEGRAM_BOT_TOKEN}/{file_path}"
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
