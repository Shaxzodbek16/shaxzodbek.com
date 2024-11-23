import os
import sys
import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import (
    KeyboardButton,
    ReplyKeyboardMarkup,
    Message,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    CallbackQuery,
    FSInputFile,
)
from aiogram.filters import CommandStart
from aiogram import F

from bot.extentions import create_user, download_youtube_video
from config import load_config

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

config = load_config()
TOKEN = config.bot.token

dp = Dispatcher()
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))


@dp.message(CommandStart())
async def start_command(message: Message):
    name = message.from_user.first_name
    reply = (
        f"Hello <b>{name}</b>! \nWelcome to our bot for downloading <b>YouTube</b> and <b>Instagram</b> videos."
    )
    create_user(
        user_id=message.from_user.id,
        first_name=name,
        last_name=message.from_user.last_name,
        username=message.from_user.username,
    )
    await message.answer("Send the video URL to download...")


@dp.message(F.text == 'Help')
async def help_command(message: Message):
    reply = "This bot allows you to download YouTube videos. Simply send a YouTube URL."
    await message.answer(
        reply,
        reply_markup=ReplyKeyboardMarkup(
            resize_keyboard=True, keyboard=[[KeyboardButton(text='Back')]]
        ),
    )


@dp.message(F.text == 'About')
async def about_command(message: Message):
    reply = "This is a YouTube video downloader bot."
    await message.answer(
        reply,
        reply_markup=ReplyKeyboardMarkup(
            resize_keyboard=True, keyboard=[[KeyboardButton(text='Back')]]
        ),
    )


user_video_urls = {}


@dp.message(F.text.startswith(('https://www.youtube.com/', 'https://youtu.be', 'https://youtube.com/')))
async def video_download(message: Message):
    url = message.text.strip()
    user_video_urls[message.message_id] = url

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text='Download Video', callback_data=f'download|video|{message.message_id}'
                )
            ],
            [
                InlineKeyboardButton(
                    text='Download MP3', callback_data=f'download|mp3|{message.message_id}'
                )
            ],
        ]
    )
    await message.answer("Select an option:", reply_markup=keyboard)


@dp.callback_query(F.data.startswith('download'))
async def handle_download_callback(query: CallbackQuery):
    _, file_type, message_id = query.data.split('|')
    message_id = int(message_id)
    url = user_video_urls.get(message_id)
    if not url:
        await query.message.answer("Sorry, I could not find the video URL. Please try again.")
        return

    await query.message.answer("Your file is being downloaded...")
    try:
        # Determine whether to download a video or MP3
        if file_type == 'mp3':
            filename = await download_youtube_video(url, mp3=True)
        elif file_type == 'video':
            filename = await download_youtube_video(url)

        file_size = os.path.getsize(filename)
        max_file_size = 50 * 1024 * 1024 * 40  # 2000 MB file size limit

        if file_size > max_file_size:
            await query.message.answer("The file is too large to send via Telegram.")
            os.remove(filename)
            return

        media = FSInputFile(filename)
        if file_type == 'mp3':
            await query.message.answer_audio(audio=media)
        else:
            await query.message.answer_video(video=media)

        os.remove(filename)
        del user_video_urls[message_id]
    except Exception as e:
        await query.message.answer("An error occurred while processing your request. Please try again later.")
        logging.error(f"Error in handle_download_callback: {e}")


async def main():
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
