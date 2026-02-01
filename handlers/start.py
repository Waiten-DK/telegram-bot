"""
Обработчик главного меню
"""
from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery

from config import WELCOME_TEXT, HELP_TEXT
from keyboards import get_main_menu

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    """Команда /start"""
    await message.answer(
        WELCOME_TEXT,
        reply_markup=get_main_menu()
    )


@router.message(Command("help"))
@router.message(F.text == "❓ Нужна помощь?")
async def cmd_help(message: Message):
    """Помощь"""
    await message.answer(
        HELP_TEXT,
        reply_markup=get_main_menu()
    )


@router.callback_query(F.data == "back_to_menu")
async def back_to_menu(callback: CallbackQuery):
    """Возврат в главное меню"""
    await callback.message.edit_text(
        WELCOME_TEXT
    )
    await callback.answer()
