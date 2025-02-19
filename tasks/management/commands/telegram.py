import os
import logging
import signal

from django.core.management.base import BaseCommand

from asgiref.sync import async_to_sync
from aiogram import Bot, Dispatcher
from aiogram.utils import executor


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TG_API_KEY = os.getenv('TG_API_KEY')
CHAT_ID = os.getenv('CHAT_ID')

if not TG_API_KEY or not CHAT_ID:
    raise ValueError(
        "TG_API_KEY or CHAT_ID is not set in environment variables."
        )

bot = Bot(token=TG_API_KEY)
dp = Dispatcher(bot)


async def send_telegram_message(message):
    try:
        await bot.send_message(chat_id=CHAT_ID, text=message)
        logger.info(f"Message sent to chat {CHAT_ID}")
    except Exception as e:
        logger.error(f"Failed to send message: {e}")


def send_message_sync(message):
    async_to_sync(send_telegram_message)(message)


class Command(BaseCommand):
    help = 'Start Telegram bot'

    def handle(self, *args, **kwargs):
        def shutdown(signal, frame):
            self.stdout.write(self.style.SUCCESS('Shutting down bot...'))
            dp.stop_polling()
            exit(0)
        signal.signal(signal.SIGINT, shutdown)
        signal.signal(signal.SIGTERM, shutdown)
        self.stdout.write(self.style.SUCCESS('Starting bot...'))
        executor.start_polling(dp, skip_updates=True)
