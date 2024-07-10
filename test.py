import yt_dlp

# URL видео, которое вы хотите загрузить
video_url = 'https://www.youtube.com/watch?v=8RlFBXilhGY'

# Настройки загрузки
ydl_opts = {
    'format': 'best',  # Выбирает лучшее качество видео
    'outtmpl': '%(title)s.%(ext)s',  # Шаблон названия файла
}

# Создание экземпляра yt-dlp и загрузка видео
with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download([video_url])
