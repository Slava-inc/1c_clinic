from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import KeyboardButton

class KeyboardBuilder:
    @staticmethod
    def build_main_menu():
        builder = ReplyKeyboardBuilder()
        builder.add(
            KeyboardButton(text="Записаться на прием"),
            KeyboardButton(text="Получить анализы"),
            KeyboardButton(text="Онлайн-консультация")
        )
        builder.adjust(2)
        return builder.as_markup(resize_keyboard=True)

    @staticmethod
    def build_confirmation():
        builder = ReplyKeyboardBuilder()
        builder.add(
            KeyboardButton(text="Да"),
            KeyboardButton(text="Нет")
        )
        builder.adjust(2)
        return builder.as_markup(resize_keyboard=True)

    @staticmethod
    def build_contact_request():
        """
        Создает клавиатуру с кнопкой запроса контакта.
        """
        builder = ReplyKeyboardBuilder()
        builder.button(text="Отправить контакт", request_contact=True)
        builder.adjust(1)  # Одна кнопка в строке
        return builder.as_markup(resize_keyboard=True)