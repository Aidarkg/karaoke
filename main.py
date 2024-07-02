import logging
from aiogram import executor
from config import dp
from handlers import start

logging.basicConfig(level=logging.INFO)
# async def on_startup(_):
#

start.register_handlers(dp)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
