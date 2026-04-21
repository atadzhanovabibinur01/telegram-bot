import asyncio 
import logging
import os

from aiogram import Bot, Dispatcher, F
from aiogram.types import (
    Message,
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery,
    FSInputFile
)
from aiogram.filters import CommandStart

import yt_dlp

API_TOKEN = "8757587179:AAHt87aQynrNAjlK1zDSUnYdCAjOaPcm0x8"

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

main_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📥 Video yuklash")],
        [KeyboardButton(text="ℹ️ Yordam")]
    ],
    resize_keyboard=True
)

inline_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="📥 Yuklashni boshlash", callback_data="start_download")]
    ]
)

def download_video(url):
    try:
        ydl_opts = {
            'outtmpl': 'downloads/%(title)s.%(ext)s',
            'format': 'best'
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

        return filename
    except Exception as e:
        print(e)
        return None


@dp.message(CommandStart())
async def start_handler(message: Message):
    await message.answer(
        "👋 Xush kelibsiz!\n\n Video yuklash uchun tugmani bosing 👇",
        reply_markup=main_kb
    )


@dp.message(F.text == "📥 Video yuklash")
async def ask_link(message: Message):
    await message.answer(
        "🔗 Video link yuboring",
        reply_markup=inline_kb
    )

@dp.message(F.text == "ℹ️ Yordam")
async def help_handler(message: Message):
    await message.answer(
        "📌 Qanday ishlaydi:\n"
        "1. 📥 Video yuklash tugmasini bosing\n"
        "2. Link yuboring\n"
        "3. Bot videoni yuklab beradi"
    )


@dp.callback_query(F.data == "start_download")
async def start_download_callback(callback: CallbackQuery):
    await callback.message.answer("🔗 Endi link yuboring")
    await callback.answer()


@dp.message(F.text)
async def download_handler(message: Message):
    url = message.text.strip()

    if "http" not in url:
        return

    await message.answer("⏳ Yuklab olinmoqda...")

    os.makedirs("downloads", exist_ok=True)

    file_path = download_video(url)

    if not file_path or not os.path.exists(file_path):
        await message.answer("❌ Xatolik yuz berdi")
        return

    video = FSInputFile(file_path)

    try:
        await message.answer_video(video)
    except:
        await message.answer_document(video)

    os.remove(file_path)


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
