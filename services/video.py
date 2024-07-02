import os
import time
import uuid

import ffmpeg
from decouple import config

from youtube_download import download_video


def generate_title():
    current_day = time.strftime("%Y%m%d")
    unique_id = uuid.uuid4().hex[:8]
    filename = f"{current_day}-{unique_id}"
    return filename


def audio_extract(url=None, path=None):
    if url:
        video_path = download_video(url)
    elif path:
        video_path = path

    file_name = generate_title()
    file_name_ext = f"{file_name}.mp3"
    print(video_path)

    audio_output_dir = config("AUDIO")
    os.makedirs(audio_output_dir, exist_ok=True)

    audio_path = os.path.join(audio_output_dir, file_name_ext)

    stream = ffmpeg.input(video_path)
    stream = ffmpeg.output(stream, audio_path, acodec='libmp3lame', audio_bitrate='192K')

    ffmpeg.run(stream)

    title_ext = {
        "title": file_name,
        "ext": ".mp3",
        "path": audio_path
    }
    return title_ext
