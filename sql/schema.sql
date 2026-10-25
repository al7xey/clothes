-- Схема базы данных системы учета размеров одежды (ПР7).
PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS items;
DROP TABLE IF EXISTS measurements;
DROP TABLE IF EXISTS parameters;
DROP TABLE IF EXISTS users;

CREATE TABLE users (
    id    INTEGER PRIMARY KEY,
    name  TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE
);

CREATE TABLE parameters (
    id        INTEGER PRIMARY KEY,
    name      TEXT NOT NULL UNIQUE,
    unit      TEXT NOT NULL,
    min_value REAL NOT NULL,
    max_value REAL NOT NULL,
    CHECK (min_value < max_value)
);

CREATE TABLE measurements (
    id           INTEGER PRIMARY KEY,
    user_id      INTEGER NOT NULL REFERENCES users (id),
    parameter_id INTEGER NOT NULL REFERENCES parameters (id),
    amount       REAL NOT NULL,
    value_date   TEXT NOT NULL
);

CREATE TABLE items (
    id      INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users (id),
    name    TEXT NOT NULL,
    size    TEXT NOT NULL
);

CREATE INDEX idx_measurements_user ON measurements (user_id);
CREATE INDEX idx_measurements_date ON measurements (value_date);
CREATE INDEX idx_items_user ON items (user_id);
