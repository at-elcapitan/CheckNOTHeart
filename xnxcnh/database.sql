DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS data_press;

CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password INTEGER NOT NULL,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    last_press TEXT DEFAULT "NONE",
    last_rate TEXT DEFAULT "NONE",
    img_url TEXT,
    admin_override BOOL NOT NULL
);

CREATE TABLE data_press (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date SMALLDATETIME NOT NULL,
    press_high INTEGER NOT NULL,
    press_low INTEGER NOT NULL,
    heart_rate INTEGER NOT NULL,
    user_state BOOL NOT NULL,
    arm TEXT NOT NULL,
    user_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES user (id)
);

INSERT INTO users (username, password, first_name, last_name, admin_override) VALUES ('root', 'pbkdf2:sha256:600000$x2BbGmc8Uj0PVPnY$275897aa0272aa2d247a8c856c8153d94264b5b52b6ef55fe7cfb899f50bac75', 'SYSTEM', 'USER', 1);
