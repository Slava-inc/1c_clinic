from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import KeyboardButton

class KeyboardBuilder:
    @staticmethod
    def build_main_menu():
        builder = ReplyKeyboardBuilder()
        builder.add(
            KeyboardButton(text="Записаться на прием"),
            KeyboardButton(text="Вызов врача на дом"),
            KeyboardButton(text="Онлайн-консультация"),
            KeyboardButton(text="Справки для налоговой"),
            KeyboardButton(text="Получить анализы"),
            KeyboardButton(text="Настройки")            
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
    
    @staticmethod
    def build_specialties_keyboard(specialties):
        builder = ReplyKeyboardBuilder()
        for specialty in specialties:
            builder.add(
                KeyboardButton(text=specialty)
            )
        builder.adjust(2)
        return builder.as_markup(resize_keyboard=True)

    @staticmethod
    def build_period_selection():
        builder = ReplyKeyboardBuilder()
        builder.add(
            KeyboardButton(text="За последний месяц"),
            KeyboardButton(text="За последние 3 месяца"),
            KeyboardButton(text="Все")
        )
        builder.adjust(3)
        return builder.as_markup(resize_keyboard=True)

    @staticmethod
    def build_certificate_types():
        builder = ReplyKeyboardBuilder()
        builder.add(
            KeyboardButton(text="Для налоговой"),
            KeyboardButton(text="Для работодателя")
        )
        builder.adjust(2)
        return builder.as_markup(resize_keyboard=True)   

    @staticmethod
    def build_doctors_keyboard(doctors):
        """
        Создает клавиатуру с врачами.
        
        :param doctors: Список словарей, где каждый словарь содержит данные о враче:
                        [{'id': 1, 'name': 'Иванов И.И.', 'specialization': 'Терапевт'}, ...]
        :return: Объект клавиатуры для Telegram.
        """
        builder = ReplyKeyboardBuilder()
        
        # Добавляем кнопки для каждого врача
        for doctor in doctors:
            button_text = f"{doctor[1]} ({doctor[2]})"
            builder.add(KeyboardButton(text=button_text))
        
        # Размещаем кнопки в две колонки
        builder.adjust(2)
        
        # Возвращаем клавиатуру
        return builder.as_markup(resize_keyboard=True) 