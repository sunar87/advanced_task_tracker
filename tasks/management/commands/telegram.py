import os
import logging
import signal
import requests

from django.core.management.base import BaseCommand

from asgiref.sync import async_to_sync
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import executor
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TG_API_KEY = os.getenv('TG_API_KEY')
CHAT_ID = os.getenv('CHAT_ID')
DJANGO_SERVER_URL = os.getenv('DJANGO_SERVER_URL')

if not TG_API_KEY or not CHAT_ID:
    raise ValueError(
        "TG_API_KEY or CHAT_ID is not set in environment variables."
        )

bot = Bot(token=TG_API_KEY)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


async def send_telegram_message(message):
    try:
        await bot.send_message(chat_id=CHAT_ID, text=message)
        logger.info(f"Message sent to chat {CHAT_ID}")
    except Exception as e:
        logger.error(f"Failed to send message: {e}")


def send_message_sync(message):
    async_to_sync(send_telegram_message)(message)


class UserData(StatesGroup):
    waiting_for_email = State()
    waiting_for_confirmation = State()


@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message, state: FSMContext):
    await message.answer("Пожалуйста, введите ваш email:")
    await UserData.waiting_for_email.set()


@dp.message_handler(state=UserData.waiting_for_email)
async def process_email(message: types.Message, state: FSMContext):
    email = message.text
    await state.update_data(email=email)
    await message.answer(
        f"Ваш email: {email}. Нажмите кнопку, чтобы передать ваш ID."
        )

    keyboard = InlineKeyboardMarkup(row_width=1)
    button = InlineKeyboardButton("Передать свой ID", callback_data='send_id')
    keyboard.add(button)

    await message.answer(
        f"Передать ваш ID: {message.from_user.id}", reply_markup=keyboard
        )
    await UserData.waiting_for_confirmation.set()


@dp.callback_query_handler(
        lambda callback_query: callback_query.data == 'send_id',
        state=UserData.waiting_for_confirmation
        )
async def process_callback(callback_query: types.CallbackQuery,
                           state: FSMContext):
    user_id = callback_query.from_user.id
    user_data = await state.get_data()
    email = user_data.get('email')

    try:
        response = requests.post(
            DJANGO_SERVER_URL,
            data={'telegram_id': user_id, 'email': email},
            headers={'tuna-skip-browser-warning': 'f'}
        )

        if response.status_code == 200:
            await bot.answer_callback_query(
                callback_query.id, "Ваш ID успешно передан!"
                )
        else:
            await bot.answer_callback_query(
                callback_query.id, "Ошибка при передаче ID."
                )
    except Exception as e:
        await bot.answer_callback_query(callback_query.id, f"Ошибка: {str(e)}")

    await state.finish()


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
