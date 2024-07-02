import re
import yt_dlp
from decouple import config


def download_video(url):
    output_path = config("VIDEO")

    ydl = yt_dlp.YoutubeDL()
    video_info = ydl.extract_info(url, download=False)
    title = video_info['title']
    title = re.sub(r'[^\w\s]', ' ', title)

    ydl_opts = {
        'format': 'best',
        'outtmpl': f'{output_path}/{title}.%(ext)s',
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    path = f'{output_path}{title}.mp4'
    return path
