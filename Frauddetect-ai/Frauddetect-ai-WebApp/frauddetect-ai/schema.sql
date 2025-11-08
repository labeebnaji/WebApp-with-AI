-- schema.sql

CREATE TABLE user (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    full_name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    role TEXT NOT NULL,
    github_link TEXT,
    linkedin_link TEXT,
    last_login TEXT
);

CREATE TABLE IF NOT EXISTS achievements (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    achievement_type TEXT NOT NULL,
    unlocked BOOLEAN DEFAULT FALSE,
    unlocked_at TEXT,
    FOREIGN KEY (user_id) REFERENCES user(id)
);

-- جدول المعاملات
CREATE TABLE transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    cc_num TEXT NOT NULL,
    category TEXT NOT NULL,
    amt REAL NOT NULL,
    zip TEXT,
    lat REAL,
    long REAL,
    city_pop INTEGER,
    merch_lat REAL,
    merch_long REAL,
    trans_day INTEGER,
    trans_month INTEGER,
    trans_year INTEGER,
    trans_hour INTEGER,
    trans_minute INTEGER,
    prediction INTEGER NOT NULL, -- 0 for fraud, 1 for safe
    transaction_date TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES user(id)
);

-- جدول النقاط
CREATE TABLE user_points (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    points INTEGER DEFAULT 0,
    last_updated TEXT,
    FOREIGN KEY (user_id) REFERENCES user(id)
);

-- جدول الألقاب
CREATE TABLE user_titles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    earned_at TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES user(id)
);

-- إدراج المستخدم أحمد
INSERT INTO user (id, username, full_name, email, role, github_link, linkedin_link, last_login) VALUES
(1, 'Ahmed', 'Ahmed', 'ahmed@gmail.com', 'user', 'https://github.com', 'https://linkedin.com', datetime('now'));

-- إدراج الإنجازات الأساسية
INSERT INTO achievements (user_id, achievement_type, unlocked, unlocked_at) VALUES
(1, 'finder', TRUE, datetime('now')),
(1, 'expert', FALSE, NULL),
(1, 'cyber_master', FALSE, NULL);

-- إدراج نقاط المستخدم
INSERT INTO user_points (user_id, points, last_updated) VALUES
(1, 5, datetime('now'));

-- إدراج الألقاب
INSERT INTO user_titles (user_id, title, earned_at) VALUES
(1, 'المبتدئ', datetime('now')),
(1, 'المحقق', datetime('now'));