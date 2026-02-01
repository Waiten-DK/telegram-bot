"""
Обработчик избранного
"""
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery

from database import db
from keyboards import get_favorites_keyboard, get_favorite_profile_keyboard

router = Router()


@router.message(F.text == "⭐️ Избранное")
async def show_favorites(message: Message):
    """Показ избранных анкет"""
    favorites = db.get_user_favorites(message.from_user.id)
    
    if not favorites:
        await message.answer(
            "❌ У вас пока нет избранных анкет\n\n"
            "Добавляйте анкеты в избранное при просмотре!",
            reply_markup=get_favorites_keyboard()
        )
        return
    
    text = "<b>⭐️ Ваши избранные анкеты:</b>\n\n"
    
    for profile in favorites:
        text += f"👤 <b>{profile['name']}</b>\n"
        text += f"📍 {profile['city']}, {profile['age']} лет\n"
        text += f"Telegram: @{profile['telegram']}\n\n"
    
    await message.answer(
        text,
        reply_markup=get_favorites_keyboard()
    )
    
    # Отправляем первую анкету с фото
    first_profile = favorites[0]
    await message.answer_photo(
        photo=first_profile['photos'][0],
        caption=f"<b>{first_profile['name']}</b>, {first_profile['city']}",
        reply_markup=get_favorite_profile_keyboard(first_profile['id'])
    )


@router.callback_query(F.data.startswith("fav_remove_"))
async def remove_favorite(callback: CallbackQuery):
    """Удаление из избранного"""
    try:
        profile_id = int(callback.data.split("_")[2])
    except (ValueError, IndexError):
        await callback.answer("❌ Ошибка данных")
        return
    
    db.remove_from_favorites(callback.from_user.id, profile_id)
    
    await callback.message.delete()
    await callback.answer("❌ Удалено из избранного")
