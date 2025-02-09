from decouple import config

from users.models import User
import requests
import logging

logger = logging.getLogger(__name__)

TELEGRAM_BOT_TOKEN = config('TELEGRAM_BOT_TOKEN')


def send_reminder(user_id, message):
    try:
        user = User.objects.get(id=user_id)  # Получаем пользователя

        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {"chat_id": user.telegram_chat_id, "text": message}

        response = requests.post(url, json=payload)

        if response.status_code == 200:
            logger.info(f"Напоминание отправлено пользователю {user.email}: {message}")
        else:
            logger.error(f"Ошибка при отправке сообщения: {response.text}")

    except User.DoesNotExist:
        logger.error(f"Пользователь с id {user_id} не существует.")
    except Exception as e:
        logger.error(f"Ошибка при отправке напоминания: {e}", exc_info=True)
