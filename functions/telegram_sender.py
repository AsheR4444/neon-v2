import requests
from loguru import logger

from data.models import Settings

settings = Settings()

def send_telegram_notification(text):
    try:
        url = f"https://api.telegram.org/bot{settings.telegram_bot_key}/sendMessage"
        payload = {
            "chat_id": settings.telegram_chat_id,
            "text": text
        }
        response = requests.post(url, json=payload)

        if response.status_code == 200:
            logger.info("Sent telegram notification to user!")
        else:
            logger.error(f"Error while sending notification to user: {response.status_code}: {response.text}")
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to send telegram notification: {e}")
