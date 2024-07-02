import time
import shutil

import ffmpeg
from decouple import config
from spleeter.separator import Separator

from video import audio_extract, generate_title


def separation(count, url=None, path=None):
    _path = audio_extract(url, path)
    input_path = _path.get('path')

    output_path = config("AUDIO")

    separator = Separator(f'spleeter:{count}stems')
    separator.separate_to_file(input_path, output_path)

    title = _path.get('title')
    files = {
        "title": title,
        "fonk": f'{config("AUDIO")}{title}/{config("FONK")}',
        "vocal": f'{config("AUDIO")}{title}/{config("VOCAL")}'
    }
    return files


def convert_mp3(count, url=None, path=None):
    _path = separation(count, url, path)
    input_path = _path.get('fonk')

    output_dir = config("AUDIO")
    filename = generate_title()
    output_path = f'{output_dir}{filename}.mp3'

    ffmpeg.input(input_path).output(output_path, audio_bitrate='192K').run()

    title = _path.get('title')
    shutil.rmtree(f'{output_dir}{title}')

    return output_path


if __name__ == "__main__":
    start_time = time.time()

    convert_mp3(2, path='media/video/Мухтар Хордаев - Небо над землей (Lyrics Video).mp4')

    end_time = time.time()
    print("Duration: {:.2f} seconds".format(end_time - start_time))
