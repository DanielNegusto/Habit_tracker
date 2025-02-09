import logging
from django.core.management.base import BaseCommand
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)
from django.contrib.auth import get_user_model
from asgiref.sync import sync_to_async

User = get_user_model()

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

httpx_logger = logging.getLogger("httpx")
httpx_logger.setLevel(logging.WARNING)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Пожалуйста, введите свой email:")


async def handle_email(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    email = update.message.text.strip()

    logger.info(f"Получен email: {email}, chat_id: {chat_id}")

    try:
        user = await sync_to_async(User.objects.get)(email=email)
        user.telegram_chat_id = chat_id
        await sync_to_async(user.save)()
        await update.message.reply_text("Ваш telegram_chat_id сохранен!")
    except User.DoesNotExist:
        logger.warning(f"Пользователь с email {email} не найден.")
        await update.message.reply_text("Пользователь не найден.")
    except Exception as e:
        logger.error(f"Ошибка при обработке email: {e}", exc_info=True)
        await update.message.reply_text("Произошла ошибка. Попробуйте позже.")


class Command(BaseCommand):
    help = "Starts the Telegram bot"

    def handle(self, *args, **kwargs):
        application = (
            ApplicationBuilder()
            .token("7005564520:AAGQLzzfu51fy15ehElaGU3c9YCJqZHa3Vk")
            .build()
        )

        application.add_handler(CommandHandler("start", start))
        application.add_handler(
            MessageHandler(filters.TEXT & ~filters.COMMAND, handle_email)
        )

        application.run_polling()
