from loguru import logger

from functions.telegram_sender import send_telegram_notification
from data.models import Settings

settings = Settings()

class Notificator:
    @staticmethod
    def info(text: str):
        logger.info(text)
        if settings.telegram_notifications_enabled:
            send_telegram_notification(f'👁️ INFO | {text}')

    @staticmethod
    def error(text):
        logger.error(text)

        if settings.telegram_notifications_enabled:
            send_telegram_notification(f'🔴 ERROR | {text}')

    @staticmethod
    def exception(text):
        logger.exception(text)

        if settings.telegram_notifications_enabled:
            send_telegram_notification(f'🟡 EXCEPTION | {text}')

    @staticmethod
    def success(text):
        logger.success(text)

        if settings.telegram_notifications_enabled:
            send_telegram_notification(f'🟢 SUCCESS | {text}')