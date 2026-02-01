"""
Вспомогательный скрипт для получения file_id фотографий
Запусти этот скрипт и отправь боту любое фото - он выдаст file_id
"""
import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from config import BOT_TOKEN

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(F.photo)
async def get_photo_id(message: Message):
    """Получение file_id фотографии"""
    photo_id = message.photo[-1].file_id
    await message.answer(
        f"✅ file_id этого фото:\n\n"
        f"<code>{photo_id}</code>\n\n"
        f"Скопируй его и вставь в profiles.json",
        parse_mode="HTML"
    )
    print(f"\n📷 file_id: {photo_id}\n")

@dp.message(F.text)
async def any_message(message: Message):
    await message.answer(
        "📸 Отправь мне фото, и я дам тебе file_id для использования в боте!"
    )

async def main():
    print("🤖 Бот запущен! Отправь ему фото в Telegram")
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
