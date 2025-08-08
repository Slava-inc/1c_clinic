# bot/handlers/main_menu.py
from aiogram import Router, F
from aiogram.types import Message
from bot.keyboards.builder import KeyboardBuilder
from constants import SPECIALITIES 

main_menu_router = Router()

@main_menu_router.message(F.text == "Главное меню")
async def main_menu(message: Message):
    await message.answer(
        "Выберите действие:",
        reply_markup=KeyboardBuilder.build_main_menu()
    )

@main_menu_router.message(F.text == "Запись на прием")
async def book_appointment(message: Message):
    await message.answer(
        "Выберите специализацию врача:",
        reply_markup=KeyboardBuilder.build_specialties_keyboard(SPECIALITIES)
    )

@main_menu_router.message(F.text == "Вызов врача на дом")
async def request_home_visit(message: Message):
    await message.answer("Укажите адрес:")

@main_menu_router.message(F.text == "Онлайн-консультации")
async def start_consultation(message: Message):
    await message.answer("Начать консультацию: [ссылка]")

@main_menu_router.message(F.text == "Справки для налоговой")
async def request_tax_certificate(message: Message):
    await message.answer(
        "Выберите тип справки:",
        reply_markup=KeyboardBuilder.build_certificate_types()
    )

@main_menu_router.message(F.text == "Мои анализы")
async def view_analyses(message: Message):
    await message.answer(
        "Выберите период:",
        reply_markup=KeyboardBuilder.build_period_selection()
    )