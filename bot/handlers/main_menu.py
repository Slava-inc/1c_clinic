# bot/handlers/main_menu.py
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from bot.keyboards.builder import KeyboardBuilder
from constants import SPECIALITIES 

main_menu_router = Router()

@main_menu_router.callback_query(F.data == "Главное меню")
async def main_menu(callback: CallbackQuery):
    await callback.answer()
    await callback.message.answer(
        "Выберите действие:",
        reply_markup=KeyboardBuilder.build_main_menu()
    )

@main_menu_router.callback_query(F.data == "book_appointment")
async def book_appointment(callback: CallbackQuery):
    await callback.answer()
    await callback.message.answer(
        "Выберите специализацию врача:",
        reply_markup=KeyboardBuilder.build_specialties_keyboard(SPECIALITIES)
    )

@main_menu_router.callback_query(F.data == "request_home_visit")
async def request_home_visit(callback: CallbackQuery):
    await callback.answer()
    await callback.message.answer("Укажите адрес:")

@main_menu_router.callback_query(F.data == "start_consultation")
async def start_consultation(callback: CallbackQuery):
    await callback.answer()
    await callback.message.answer("Начать консультацию: [ссылка]")

@main_menu_router.callback_query(F.data == "request_tax_certificate")
async def request_tax_certificate(callback: CallbackQuery):
    await callback.answer()
    await callback.message.answer(
        "Выберите тип справки:",
        reply_markup=KeyboardBuilder.build_certificate_types()
    )

@main_menu_router.callback_query(F.data == "view_analyses")
async def view_analyses(callback: CallbackQuery):
    await callback.answer()
    await callback.message.answer(
        "Выберите период:",
        reply_markup=KeyboardBuilder.build_period_selection()
    )