"""
Обработчик просмотра анкет
"""
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InputMediaPhoto
from aiogram.exceptions import TelegramBadRequest

from database import db
from keyboards import get_profile_keyboard

router = Router()


def format_profile_text(profile: dict) -> str:
    """Форматирование текста анкеты"""
    text = f"""
<b>👤 {profile['name']}</b>
📍 {profile['city']}

<b>Характеристики:</b>
▪️ Возраст: {profile['age']} лет
▪️ Рост: {profile['height']} см
▪️ Вес: {profile['weight']} кг
▪️ Внешность: {profile['appearance']}

📱 <b>Контакты:</b>
▪️ Телефон: <code>{profile['phone']}</code>
▪️ Telegram: @{profile['telegram']}

📷 Фотографий: {len(profile['photos'])}
"""
    return text.strip()


@router.message(F.text == "👀 Смотреть анкеты")
async def show_profiles(message: Message):
    """Показ первой анкеты"""
    profile = db.get_profile(0)
    
    if not profile:
        await message.answer("❌ Анкеты не найдены")
        return
    
    photo_url = profile['photos'][0]
    caption = format_profile_text(profile)
    
    is_fav = db.is_favorite(message.from_user.id, profile['id'])
    
    await message.answer_photo(
        photo=photo_url,
        caption=caption,
        reply_markup=get_profile_keyboard(
            profile_id=profile['id'],
            current_photo=0,
            total_photos=len(profile['photos']),
            total_profiles=db.get_total_profiles(),
            is_favorite=is_fav
        )
    )


@router.callback_query(F.data.startswith("profile_"))
async def navigate_profile(callback: CallbackQuery):
    """
    Навигация по анкетам и фото
    Формат: profile_{profile_id}_{photo_index}
    """
    try:
        _, profile_id, photo_index = callback.data.split("_")
        profile_id = int(profile_id)
        photo_index = int(photo_index)
    except ValueError:
        await callback.answer("❌ Ошибка данных")
        return
    
    profile = db.get_profile(profile_id)
    
    if not profile:
        await callback.answer("❌ Анкета не найдена")
        return
    
    # Проверка индекса фото
    if photo_index >= len(profile['photos']):
        photo_index = 0
    
    photo_url = profile['photos'][photo_index]
    caption = format_profile_text(profile)
    
    is_fav = db.is_favorite(callback.from_user.id, profile['id'])
    
    # Обновление сообщения с новым фото
    try:
        await callback.message.edit_media(
            media=InputMediaPhoto(
                media=photo_url,
                caption=caption
            ),
            reply_markup=get_profile_keyboard(
                profile_id=profile['id'],
                current_photo=photo_index,
                total_photos=len(profile['photos']),
                total_profiles=db.get_total_profiles(),
                is_favorite=is_fav
            )
        )
    except TelegramBadRequest:
        # Если фото то же самое, просто обновляем клавиатуру
        await callback.message.edit_caption(
            caption=caption,
            reply_markup=get_profile_keyboard(
                profile_id=profile['id'],
                current_photo=photo_index,
                total_photos=len(profile['photos']),
                total_profiles=db.get_total_profiles(),
                is_favorite=is_fav
            )
        )
    
    await callback.answer()


@router.callback_query(F.data.startswith("fav_toggle_"))
async def toggle_favorite(callback: CallbackQuery):
    """Добавление/удаление из избранного"""
    try:
        profile_id = int(callback.data.split("_")[2])
    except (ValueError, IndexError):
        await callback.answer("❌ Ошибка данных")
        return
    
    user_id = callback.from_user.id
    
    if db.is_favorite(user_id, profile_id):
        db.remove_from_favorites(user_id, profile_id)
        await callback.answer("❌ Удалено из избранного")
        is_fav = False
    else:
        db.add_to_favorites(user_id, profile_id)
        await callback.answer("⭐️ Добавлено в избранное")
        is_fav = True
    
    # Обновление клавиатуры
    profile = db.get_profile(profile_id)
    if profile:
        # Получаем текущий индекс фото из caption или используем 0
        current_photo = 0
        
        try:
            await callback.message.edit_reply_markup(
                reply_markup=get_profile_keyboard(
                    profile_id=profile_id,
                    current_photo=current_photo,
                    total_photos=len(profile['photos']),
                    total_profiles=db.get_total_profiles(),
                    is_favorite=is_fav
                )
            )
        except TelegramBadRequest:
            pass
