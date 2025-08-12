import sqlite3
from datetime import datetime, timedelta

# Подключение к базе данных
conn = sqlite3.connect('clinic.db')
cursor = conn.cursor()

# Создание таблицы schedule (если она еще не существует)
cursor.execute('''
-- Заполнение таблицы specializations тестовыми данными
INSERT INTO specializations (name, home_visit_available) VALUES
('Терапевт', 1),          -- Вызов на дом доступен
('Педиатр', 1),           -- Вызов на дом доступен
('Стоматолог', 0),        -- Вызов на дом недоступен
('Хирург', 0),            -- Вызов на дом недоступен
('Гинеколог', 1),         -- Вызов на дом доступен
('Офтальмолог', 0),       -- Вызов на дом недоступен
('Невролог', 1);          -- Вызов на дом доступен
''')

conn.commit()
conn.close()