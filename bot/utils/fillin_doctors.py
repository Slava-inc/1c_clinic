import sqlite3

# Подключение к базе данных (или создание новой)
conn = sqlite3.connect('clinic.db')
cursor = conn.cursor()

# Создание таблицы doctors (если она еще не существует)
cursor.execute('''
CREATE TABLE IF NOT EXISTS doctors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    specialization TEXT NOT NULL
)
''')

# Тестовые данные: список врачей
test_doctors = [
    # Терапевты
    {"name": "Иванов Иван Иванович", "specialization": "Терапевт"},
    {"name": "Петров Петр Петрович", "specialization": "Терапевт"},
    
    # Окулисты
    {"name": "Сидорова Анна Сергеевна", "specialization": "Окулист"},
    {"name": "Кузнецов Дмитрий Александрович", "specialization": "Окулист"},
    
    # Хирурги
    {"name": "Михайлов Михаил Михайлович", "specialization": "Хирург"},
    {"name": "Федорова Елена Владимировна", "specialization": "Хирург"},
    
    # Урологи
    {"name": "Алексеев Алексей Алексеевич", "specialization": "Уролог"},
    {"name": "Николаева Ольга Николаевна", "specialization": "Уролог"},
]

# Вставка данных в таблицу
for doctor in test_doctors:
    cursor.execute('''
    INSERT INTO doctors (name, specialization)
    VALUES (?, ?)
    ''', (doctor["name"], doctor["specialization"]))

# Сохранение изменений и закрытие соединения
conn.commit()
conn.close()

print("Тестовые данные успешно добавлены в таблицу 'doctors'.")