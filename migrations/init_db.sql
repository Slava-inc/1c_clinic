-- Создание таблицы пациентов
CREATE TABLE IF NOT EXISTS patients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT NOT NULL,
    phone_number TEXT UNIQUE NOT NULL,
    email TEXT,
    date_of_birth DATE,
    telegram_id INTEGER UNIQUE,
    dms_policy TEXT, -- Полис ДМС
    oms_policy TEXT  -- Полис ОМС
);

-- Создание таблицы врачей
CREATE TABLE IF NOT EXISTS doctors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    specialization TEXT NOT NULL
);

-- Создание таблицы расписания врачей
CREATE TABLE IF NOT EXISTS schedule (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    doctor_id INTEGER NOT NULL,
    appointment_date DATETIME NOT NULL,
    status TEXT DEFAULT 'free', -- free, busy
    FOREIGN KEY(doctor_id) REFERENCES doctors(id)
);

-- Создание таблицы записей на прием
CREATE TABLE IF NOT EXISTS appointments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id INTEGER NOT NULL,
    doctor_id INTEGER NOT NULL,
    appointment_date DATETIME NOT NULL,
    status TEXT DEFAULT 'scheduled', -- scheduled, canceled, completed
    FOREIGN KEY(patient_id) REFERENCES patients(id),
    FOREIGN KEY(doctor_id) REFERENCES doctors(id)
);

-- Создание таблицы медицинских анализов
CREATE TABLE IF NOT EXISTS medical_analyses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id INTEGER NOT NULL,
    analysis_type TEXT NOT NULL,
    result_file BLOB, -- Файл с результатами (PDF/фото)
    analysis_date DATE NOT NULL,
    FOREIGN KEY(patient_id) REFERENCES patients(id)
);

-- Создание таблицы уведомлений
CREATE TABLE IF NOT EXISTS notifications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id INTEGER NOT NULL,
    notification_type TEXT NOT NULL, -- confirmation, reminder_24h, reminder_1h, post_visit
    notification_date DATETIME NOT NULL,
    status TEXT DEFAULT 'pending', -- pending, sent, failed
    FOREIGN KEY(patient_id) REFERENCES patients(id)
);

-- Создание таблицы сценариев уведомлений
CREATE TABLE IF NOT EXISTS notification_scenarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_type TEXT NOT NULL,
    time_before_appointment INTEGER NOT NULL, -- Время до приема в минутах
    message_template TEXT NOT NULL
);

-- Создание таблицы логов рассылок
CREATE TABLE IF NOT EXISTS mailing_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id INTEGER NOT NULL,
    scenario_id INTEGER NOT NULL,
    send_time DATETIME NOT NULL,
    status TEXT NOT NULL,
    FOREIGN KEY(patient_id) REFERENCES patients(id),
    FOREIGN KEY(scenario_id) REFERENCES notification_scenarios(id)
);

-- Создание таблицы specializations
CREATE TABLE IF NOT EXISTS specializations (
    id INT AUTO_INCREMENT PRIMARY KEY,          -- Уникальный идентификатор специализации
    name VARCHAR(255) NOT NULL,                 -- Название специализации
    home_visit_available BOOLEAN NOT NULL      -- Доступен ли вызов врача на дом
);

-- Создание таблицы home_visits
-- Создание таблицы home_visits
CREATE TABLE IF NOT EXISTS home_visits (
    id INTEGER PRIMARY KEY AUTOINCREMENT,          -- Уникальный идентификатор заявки
    patient_id INTEGER NOT NULL,                   -- Идентификатор пациента
    specialization_id INTEGER NOT NULL,            -- Идентификатор специализации врача
    address TEXT NOT NULL,                         -- Адрес пациента
    preferred_time TIME NOT NULL,                  -- Предпочтительное время визита
    status TEXT DEFAULT 'pending',                 -- Статус заявки (по умолчанию 'pending')
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Дата и время создания заявки
    FOREIGN KEY (specialization_id) REFERENCES specializations(id) ON DELETE CASCADE
);