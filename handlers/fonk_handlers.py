import os

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from decouple import config

from config import bot
from services.fonk import convert_mp3, video_extract


def video_main(url=None, path=None):
    audio_file = convert_mp3(2, url, path)
    audio = audio_file.get('output_path')
    video = audio_file.get('video_path')
    video_file = video_extract(audio, video)

    print(video_file)

    return video_file


async def video_handler_url(message: types.Message):
    await bot.send_message(
        message.chat.id,
        text='Началась обработка...'
    )
    
    video_file = video_main(message.text)
    with open(video_file, 'rb') as video:
        await bot.send_video(
            message.chat.id,
            video=video
        )


async def video_handler(message: types.Message, state: FSMContext):
    await bot.send_message(
        message.chat.id,
        text='Началась обработка...'
    )

    video = message.video

    # Получаем путь к файлу
    file_info = await bot.get_file(video.file_id)
    file_path = file_info.file_path

    # Скачиваем файл
    downloaded_file = await bot.download_file(file_path)

    # Сохраняем файл
    output_dir = config('VIDEO')
    os.makedirs(output_dir, exist_ok=True)
    output_file_path = os.path.join(output_dir, video.file_name)

    with open(output_file_path, 'wb') as new_file:
        new_file.write(downloaded_file.read())

    # Обрабатываем видео
    video_ext = video_main(path=output_file_path)

    # Отправляем обработанное видео обратно
    with open(video_ext, 'rb') as video_file:
        await bot.send_video(
            message.chat.id,
            video_file
        )


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(video_handler_url, content_types=types.ContentTypes.TEXT)
    dp.register_message_handler(video_handler, content_types=types.ContentTypes.VIDEO)
