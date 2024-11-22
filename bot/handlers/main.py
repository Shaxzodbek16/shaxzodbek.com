from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, Message

from bot.views.user import create_user

main_router = Router()

btn = ReplyKeyboardMarkup(resize_keyboard=True,
                          keyboard=[
                              [KeyboardButton(text='Help'), KeyboardButton(text='About')],
                          ])


@main_router.message(CommandStart())
async def start_command(message: Message):
    name = message.from_user.first_name
    create_user(user_id=message.from_user.id, first_name=name,
                last_name=message.from_user.last_name, username=message.from_user.username)
    await message.answer(
        f'Hello <b>{name}</b>! \nWelcome to our bot for downloading <b>YouTube</b> and <b>Instagram</b> videos',
        reply_markup=btn)
    await message.answer('Yuklab olish uchun video url ni jo\'nating....')


@main_router.message(F.text == 'Help')
async def help_command(message: Message):
    await message.answer('Help!')


@main_router.message(F.text == 'About')
async def about_command(message: Message):
    await message.answer('About')
