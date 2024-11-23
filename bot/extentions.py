import json
import requests
import asyncio
import os
from yt_dlp import YoutubeDL

from bot.config import load_config

config = load_config()

BASE_URL = config.api.BASE_URL


def create_user(**kwargs) -> str:
    url = BASE_URL + '/create_user/'
    user_id = kwargs.get('user_id')
    response = json.loads(requests.get(url).text)
    user_exists = False
    for i in response['results']:
        if i['user_id'] == kwargs['user_id']:
            user_exists = True
            requests.put(url + f'{user_id}/', data=kwargs)
            break
    if not user_exists:
        requests.post(url, data=kwargs)
        return 'User created successfully'
    return 'User already exists'


async def download_youtube_video(url: str, mp3: bool = False):
    """
    Download the highest quality video or audio from a YouTube URL.

    Args:
        url (str): The URL of the YouTube video to download.
        mp3 (bool): If True, download audio in MP3 format. Defaults to False.

    Returns:
        str: The filename of the downloaded file.
    """
    ydl_opts = {
        'outtmpl': os.path.join('downloads', '%(title)s.%(ext)s'),
        'quiet': True,  # Suppress console output
    }
    if mp3:
        ydl_opts.update({
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        })
    else:
        ydl_opts.update({
            'format': 'bestvideo+bestaudio/best',
            'merge_output_format': 'mp4',
        })
    loop = asyncio.get_event_loop()
    filename = await loop.run_in_executor(None, sync_download, url, ydl_opts)
    return filename


def sync_download(url, ydl_opts):
    """
    Synchronous download function to be executed in an executor.

    Args:
        url (str): The YouTube video URL to download.
        ydl_opts (dict): YouTubeDL options.

    Returns:
        str: The filename of the downloaded file.
    """
    os.makedirs('downloads', exist_ok=True)
    with YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=True)
        # For post-processed files (like MP3 extraction)
        if 'requested_downloads' in info_dict:
            # Get the last requested download's filepath
            filename = info_dict['requested_downloads'][-1]['filepath']
        elif 'filepath' in info_dict:
            # Get the filepath directly
            filename = info_dict['filepath']
        elif '_filename' in info_dict:
            filename = info_dict['_filename']
        else:
            # Fallback to prepare_filename
            filename = ydl.prepare_filename(info_dict)
    return filename

