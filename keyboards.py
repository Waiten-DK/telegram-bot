"""
Клавиатуры бота
"""
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_main_menu():
    """Главное меню"""
    keyboard = [
        [KeyboardButton(text="👀 Смотреть анкеты")],
        [KeyboardButton(text="⭐️ Избранное")],
        [KeyboardButton(text="❓ Нужна помощь?")]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


def get_profile_keyboard(profile_id: int, current_photo: int, total_photos: int, 
                         total_profiles: int, is_favorite: bool = False):
    """
    Клавиатура для просмотра анкеты
    
    Args:
        profile_id: ID текущей анкеты
        current_photo: Номер текущего фото (0-based)
        total_photos: Всего фото у анкеты
        total_profiles: Всего анкет
        is_favorite: Добавлена ли в избранное
    """
    builder = InlineKeyboardBuilder()
    
    # Кнопка избранного
    fav_text = "⭐️ Убрать из избранного" if is_favorite else "⭐️ В избранное"
    builder.row(
        InlineKeyboardButton(text=fav_text, callback_data=f"fav_toggle_{profile_id}")
    )
    
    # Навигация по анкетам
    nav_buttons = []
    if profile_id > 0:
        nav_buttons.append(
            InlineKeyboardButton(text="⬅️ Предыдущая", callback_data=f"profile_{profile_id - 1}_0")
        )
    if profile_id < total_profiles - 1:
        nav_buttons.append(
            InlineKeyboardButton(text="Следующая ➡️", callback_data=f"profile_{profile_id + 1}_0")
        )
    
    if nav_buttons:
        builder.row(*nav_buttons)
    
    # Кнопка следующего фото (если фото больше 1)
    if total_photos > 1:
        next_photo = (current_photo + 1) % total_photos
        builder.row(
            InlineKeyboardButton(
                text=f"📷 Следующее фото ({current_photo + 1}/{total_photos})",
                callback_data=f"profile_{profile_id}_{next_photo}"
            )
        )
    
    # Кнопка назад
    builder.row(
        InlineKeyboardButton(text="🔙 Назад в меню", callback_data="back_to_menu")
    )
    
    return builder.as_markup()


def get_favorites_keyboard():
    """Клавиатура для избранного"""
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="🔙 Назад в меню", callback_data="back_to_menu")
    )
    return builder.as_markup()


def get_favorite_profile_keyboard(profile_id: int):
    """Клавиатура для анкеты из избранного"""
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="👀 Открыть анкету", callback_data=f"profile_{profile_id}_0")
    )
    builder.row(
        InlineKeyboardButton(text="❌ Удалить из избранного", callback_data=f"fav_remove_{profile_id}")
    )
    return builder.as_markup()
