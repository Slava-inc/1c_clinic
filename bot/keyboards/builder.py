from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from aiogram.types import InlineKeyboardButton, KeyboardButton

class KeyboardBuilder:
    @staticmethod
    def build_main_menu():
        builder = InlineKeyboardBuilder()
        builder.add(
            InlineKeyboardButton(text="Записаться на прием", callback_data='schedule_appointment'),
            InlineKeyboardButton(text="Вызов врача на дом", callback_data='home_visit'),
            InlineKeyboardButton(text="Онлайн-консультация", callback_data='start_consultation'),
            InlineKeyboardButton(text="Справки для налоговой", callback_data='request_tax_certificate'),
            InlineKeyboardButton(text="Получить анализы", callback_data='view_analyses'),
            # InlineKeyboardButton(text="Настройки", callback_data='')            
        )
        builder.adjust(2)
        return builder.as_markup(resize_keyboard=True)

    @staticmethod
    def build_confirmation():
        """
        Создает инлайн-клавиатуру для подтверждения действия.
        """
        builder = InlineKeyboardBuilder()
        builder.add(
            InlineKeyboardButton(text="Да", callback_data="confirm_yes"),
            InlineKeyboardButton(text="Нет", callback_data="confirm_no")
        )
        builder.adjust(2)  # Размещаем кнопки в две колонки
        return builder.as_markup()

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
        Создает инлайн-клавиатуру с врачами.
        
        :param doctors: Список словарей, где каждый словарь содержит данные о враче:
                        [{'id': 1, 'name': 'Иванов И.И.', 'specialization': 'Терапевт'}, ...]
        :return: Объект клавиатуры для Telegram.
        """
        builder = InlineKeyboardBuilder()
        for doctor in doctors:
            button_text = f"{doctor['name']} ({doctor['specialization']})"
            builder.add(
                InlineKeyboardButton(
                    text=button_text,
                    callback_data=f"doctor_{doctor['id']}"
                )
            )
        builder.adjust(2)  # Размещаем кнопки в две колонки

        # Отладочный вывод (упрощенный)
        # print("Клавиатура врачей:")
        # for row in builder.export():
        #     print([{"text": btn.text, "callback_data": btn.callback_data} for btn in row])

        return builder.as_markup(resize_keyboard = True)
    
    @staticmethod
    def build_schedule_keyboard(schedule):
        """
        Создает инлайн-клавиатуру со свободными слотами времени.
        
        :param schedule: Список словарей, где каждый словарь содержит данные о слоте:
                        [{'appointment_date': '2024-07-10 09:00'}, ...]
        :return: Объект клавиатуры для Telegram.
        """
        builder = InlineKeyboardBuilder()
        for slot in schedule:
            appointment_date = slot["appointment_date"]
            builder.add(
                InlineKeyboardButton(
                    text=appointment_date,
                    callback_data=f"slot_{slot['doctor_id']}_{appointment_date}"
                )
            )
        builder.adjust(3)  # Размещаем кнопки в три колонки
        return builder.as_markup()  

    @staticmethod
    def build_home_visit_specializations(specializations):
        """
        Создает клавиатуру для выбора специализации врача.
        
        :param specializations: Список специализаций, например:
                                [{'id': 1, 'name': 'Терапевт'}, {'id': 2, 'name': 'Педиатр'}]
        :return: Объект клавиатуры для Telegram.
        """
        builder = InlineKeyboardBuilder()
        for spec in specializations:
            builder.add(
                InlineKeyboardButton(
                    text=spec['name'],
                    callback_data=f"home_visit_spec_{spec['id']}"
                )
            )
        builder.adjust(2)  # Размещаем кнопки в две колонки
        return builder.as_markup()  