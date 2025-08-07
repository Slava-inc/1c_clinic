from aiogram.utils.keyboard import ReplyKeyboardBuilder

class KeyboardBuilder:
    @staticmethod
    def build_main_menu():
        builder = ReplyKeyboardBuilder()
        builder.add("Записаться на прием", "Получить анализы", "Онлайн-консультация")
        builder.adjust(2)
        return builder.as_markup(resize_keyboard=True)

    @staticmethod
    def build_confirmation():
        builder = ReplyKeyboardBuilder()
        builder.add("Да", "Нет")
        builder.adjust(2)
        return builder.as_markup(resize_keyboard=True)