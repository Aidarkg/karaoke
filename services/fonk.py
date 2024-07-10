import shutil
import subprocess
import time

import ffmpeg
from decouple import config
from spleeter.separator import Separator

from services.video import audio_extract, generate_title


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
        "vocal": f'{config("AUDIO")}{title}/{config("VOCAL")}',
        "video_path": _path.get('video_path')
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

    files = {
        "output_path": output_path,
        "video_path": _path.get('video_path')
    }

    return files


def video_extract(audio_path, video_path):
    output_path = f'{video_path}-edited.mp4'

    cmd = [
        'ffmpeg',
        '-y',
        '-i', video_path,
        '-i', audio_path,
        '-c:v', 'copy',
        '-c:a', 'aac',
        '-strict', 'experimental',
        '-map', '0:v:0',
        '-map', '1:a:0',
        output_path
    ]

    subprocess.run(cmd, check=True)

    return output_path


# if __name__ == "__main__":
#     start_time = time.time()
#
#     audio_file = convert_mp3(2, url='https://youtu.be/u3k4zdSSt-M?si=MqlqulN8tnTAofC8')
#     audio = audio_file.get('output_path')
#     video = audio_file.get('video_path')
#
#     video_file = video_extract('media/audio/20240710-b1d6085f.mp3', 'media/video/Мухтар Хордаев   Небо над землей  Lyrics Video .mp4')
#     print(video_file)
#
#     end_time = time.time()
#     print("Duration: {:.2f} seconds".format(end_time - start_time))
