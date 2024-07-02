from aiogram import Dispatcher, types
from config import bot


async def start_menu(message: types.Message):
    await bot.send_message(
        message.chat.id,
        text='Привет, пришли ссылку на Youtube или видео'
    )


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(start_menu, commands="start")
