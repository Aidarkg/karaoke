from aiogram import types


async def keyboard():
    markup = types.InlineKeyboardMarkup()
    start = types.InlineKeyboardButton(
        "Aidar",
        callback_data='dd'
    )
    markup.add(start)
    return markup