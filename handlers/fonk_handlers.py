from aiogram import Dispatcher, types
from config import bot
from services.fonk import convert_mp3, video_extract


def video_main(url=None, path=None):
    audio_file = convert_mp3(2, url, path)
    audio = audio_file.get('output_path')
    video = audio_file.get('video_path')
    video_file = video_extract(audio, video)

    print(video_file)

    return video_file


async def video_handler(message: types.Message):
    video_file = video_main(message.text)
    with open(video_file, 'rb') as video:
        await bot.send_video(
            message.chat.id,
            video=video
        )


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(video_handler, content_types=types.ContentTypes.TEXT)