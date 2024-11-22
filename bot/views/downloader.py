from bot.config import load_config

config = load_config()
import os
from yt_dlp import YoutubeDL
import os
from yt_dlp import YoutubeDL


class VideoNotDownloaded(Exception):
    def __init__(self, url, message):
        self.url = url
        self.message = message

class Downloader:
    def __init__(self, url: str, quality: str = '720p'):
        self.url = url
        self.quality = quality
        self.download_dir = 'downloads'
        if isinstance(self.download_dir, tuple):
            self.download_dir = self.download_dir[0]
        elif not isinstance(self.download_dir, str):
            self.download_dir = 'downloads'
        self.instagram_username = config.instagram.username
        self.instagram_password = config.instagram.password

    def __is_instagram_reel(self):
        return self.url.startswith("https://www.instagram.com/reel/")

    def __is_instagram_story(self):
        return self.url.startswith("https://www.instagram.com/stories/")

    def __is_youtube(self):
        return self.url.startswith('https://youtu.be/') or self.url.startswith('https://www.youtube.com/watch?v=')

    def download(self):
        if self.__is_instagram_reel():
            self.__download_instagram_reel()
        elif self.__is_instagram_story():
            self.__download_instagram_story()
        elif self.__is_youtube():
            self.__download_youtube_video()
        else:
            raise VideoNotDownloaded(self.url, 'Could not download video.')

    def __download_instagram_reel(self):
        os.makedirs(self.download_dir, exist_ok=True)
        ydl_opts = {
            'outtmpl': os.path.join(self.download_dir, '%(uploader)s/%(title)s.%(ext)s'),
        }
        if self.instagram_username and self.instagram_password:
            ydl_opts.update({
                'username': self.instagram_username,
                'password': self.instagram_password,
            })
        try:
            with YoutubeDL(ydl_opts) as ydl:
                ydl.download([self.url])
        except Exception as e:
            raise VideoNotDownloaded(self.url, str(e))

    def __download_instagram_story(self):
        os.makedirs(self.download_dir, exist_ok=True)
        ydl_opts = {
            'outtmpl': os.path.join(self.download_dir, '%(uploader)s/%(title)s.%(ext)s'),
        }
        if self.instagram_username and self.instagram_password:
            ydl_opts.update({
                'username': self.instagram_username,
                'password': self.instagram_password,
                'cookiesfrombrowser': ('chrome',),
            })
        else:
            raise VideoNotDownloaded(self.url, 'Instagram authentication is required to download stories.')
        try:
            with YoutubeDL(ydl_opts) as ydl:
                ydl.download([self.url])
        except Exception as e:
            raise VideoNotDownloaded(self.url, str(e))

    def __download_youtube_video(self):
        os.makedirs(self.download_dir, exist_ok=True)
        ydl_opts = {
            'outtmpl': os.path.join(self.download_dir, '%(title)s.%(ext)s'),
        }
        if self.quality == 'mp3':
            ydl_opts.update({
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
            })
        else:
            quality_number = ''.join(filter(str.isdigit, self.quality))
            if not quality_number:
                raise VideoNotDownloaded(self.url, f'Invalid quality: {self.quality}')
            ydl_opts.update({
                'format': f'bestvideo[height<={quality_number}]+bestaudio/best[height<={quality_number}]',
                'merge_output_format': 'mp4',
            })
        try:
            with YoutubeDL(ydl_opts) as ydl:
                ydl.download([self.url])
        except Exception as e:
            raise VideoNotDownloaded(self.url, str(e))

    def __str__(self):
        return self.url

    def __repr__(self):
        return f"{self.url} {self.__class__.__name__}"

    def __hash__(self):
        return hash(self.url)

    def __eq__(self, other):
        return self.url == other.url

# # Download a YouTube video at 1080p
# downloader = Downloader('https://www.youtube.com/watch?v=dQw4w9WgXcQ', quality='1080p')
# downloader.download()
#
# # Download a YouTube video as MP3
# downloader = Downloader('https://www.youtube.com/watch?v=dQw4w9WgXcQ', quality='mp3')
# downloader.download()

# Download an Instagram reel
# downloader = Downloader('https://www.instagram.com/reel/XXXXXXX/')
# downloader.download()
#
# Download an Instagram story (requires authentication)
downloader = Downloader('https://www.instagram.com/stories/komron_production_/3505996085734742828?utm')
downloader.download()
