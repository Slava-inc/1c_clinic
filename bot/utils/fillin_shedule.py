import sqlite3
from datetime import datetime, timedelta

# Подключение к базе данных
conn = sqlite3.connect('clinic.db')
cursor = conn.cursor()

# Создание таблицы schedule (если она еще не существует)
cursor.execute('''
CREATE TABLE IF NOT EXISTS schedule (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    doctor_id INTEGER NOT NULL,
    appointment_date TEXT NOT NULL,
    status TEXT NOT NULL,
    FOREIGN KEY (doctor_id) REFERENCES doctors (id)
)
''')

# Функция для генерации расписания
def generate_schedule(doctor_id, start_date, days=7):
    """
    Генерирует расписание для врача на указанное количество дней.
    
    :param doctor_id: ID врача из таблицы doctors.
    :param start_date: Дата начала расписания (строка в формате YYYY-MM-DD).
    :param days: Количество дней для генерации расписания.
    :return: Список слотов расписания.
    """
    schedule = []
    current_date = datetime.strptime(start_date, "%Y-%m-%d")
    
    for _ in range(days):
        # Генерация слотов на текущий день
        for hour in range(9, 18):  # Рабочие часы: с 9:00 до 17:00
            slot_time = f"{current_date.strftime('%Y-%m-%d')} {hour}:00"
            status = "free" if hour % 2 == 0 else "busy"  # Чередуем свободные и занятые слоты
            schedule.append((doctor_id, slot_time, status))
        
        # Переход к следующему дню
        current_date += timedelta(days=1)
    
    return schedule

# Получение списка врачей из таблицы doctors
cursor.execute("SELECT id FROM doctors")
doctors = cursor.fetchall()

# Генерация расписания для каждого врача
start_date = "2024-07-10"  # Начальная дата для генерации расписания
for doctor in doctors:
    doctor_id = doctor[0]
    schedule = generate_schedule(doctor_id, start_date)
    
    # Вставка данных в таблицу schedule
    cursor.executemany('''
    INSERT INTO schedule (doctor_id, appointment_date, status)
    VALUES (?, ?, ?)
    ''', schedule)

# Сохранение изменений и закрытие соединения
conn.commit()
conn.close()

print("Тестовые данные успешно добавлены в таблицу 'schedule'.")