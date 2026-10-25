-- SQL-запросы приложения. Каждый запрос помечен комментарием "-- name:".

-- name: list_parameters
-- Простая выборка: все параметры
SELECT id, name, unit, min_value, max_value
FROM parameters
ORDER BY id;

-- name: list_users
-- Простая выборка: все пользователи
SELECT id, name, email
FROM users
ORDER BY name;

-- name: parameter_by_id
-- Условие WHERE: параметр по идентификатору
SELECT id, name, unit, min_value, max_value
FROM parameters
WHERE id = ?;

-- name: measurements_by_date
-- Условие WHERE + JOIN: мерки за выбранную дату
SELECT m.id, u.name AS user_name, p.name AS parameter_name,
       p.unit, m.amount, m.value_date
FROM measurements AS m
JOIN users AS u ON u.id = m.user_id
JOIN parameters AS p ON p.id = m.parameter_id
WHERE m.value_date = ?
ORDER BY m.id;

-- name: measurements_of_user
-- Условие WHERE + JOIN: все мерки пользователя
SELECT m.id, p.name AS parameter_name, p.unit, m.amount, m.value_date
FROM measurements AS m
JOIN parameters AS p ON p.id = m.parameter_id
WHERE m.user_id = ?
ORDER BY m.value_date, m.id;

-- name: list_measurements
-- JOIN: мерки вместе с пользователем и параметром
SELECT m.id, u.name AS user_name, p.name AS parameter_name,
       p.unit, m.amount, m.value_date
FROM measurements AS m
JOIN users AS u ON u.id = m.user_id
JOIN parameters AS p ON p.id = m.parameter_id
ORDER BY m.id;

-- name: measurement_by_id
-- JOIN + WHERE: одна мерка с проверкой допустимого диапазона
SELECT m.id, u.name AS user_name, p.name AS parameter_name, p.unit,
       m.amount, m.value_date,
       (m.amount BETWEEN p.min_value AND p.max_value) AS in_range
FROM measurements AS m
JOIN users AS u ON u.id = m.user_id
JOIN parameters AS p ON p.id = m.parameter_id
WHERE m.id = ?;

-- name: list_items
-- JOIN: вещи вместе с владельцами
SELECT i.id, i.name, i.size, i.user_id, u.name AS user_name
FROM items AS i
JOIN users AS u ON u.id = i.user_id
ORDER BY i.id;

-- name: item_by_id
-- JOIN + WHERE: одна вещь с владельцем
SELECT i.id, i.name, i.size, i.user_id, u.name AS user_name
FROM items AS i
JOIN users AS u ON u.id = i.user_id
WHERE i.id = ?;

-- name: latest_amount
-- WHERE + сортировка: последняя мерка параметра у пользователя
SELECT amount
FROM measurements
WHERE user_id = ? AND parameter_id = ?
ORDER BY value_date DESC, id DESC
LIMIT 1;

-- name: count_measurements
-- COUNT: общее число мерок
SELECT COUNT(*) AS total
FROM measurements;

-- name: count_items
-- COUNT: общее число вещей
SELECT COUNT(*) AS total
FROM items;

-- name: count_users
-- COUNT: общее число пользователей
SELECT COUNT(*) AS total
FROM users;

-- name: measurements_per_parameter
-- GROUP BY: число мерок и среднее значение по каждому параметру
SELECT p.name AS parameter_name, p.unit,
       COUNT(m.id) AS total, ROUND(AVG(m.amount), 1) AS average
FROM parameters AS p
LEFT JOIN measurements AS m ON m.parameter_id = p.id
GROUP BY p.id
ORDER BY p.id;

-- name: items_per_user
-- GROUP BY: число вещей у каждого пользователя
SELECT u.name AS user_name, COUNT(i.id) AS total
FROM users AS u
LEFT JOIN items AS i ON i.user_id = u.id
GROUP BY u.id
ORDER BY u.id;

-- name: measurements_per_user
-- GROUP BY + HAVING: пользователи, у которых не меньше N мерок
SELECT u.name AS user_name, COUNT(m.id) AS total
FROM users AS u
JOIN measurements AS m ON m.user_id = u.id
GROUP BY u.id
HAVING COUNT(m.id) >= ?
ORDER BY total DESC, u.name;

-- name: measurement_dates
-- GROUP BY: даты, в которые проводились замеры
SELECT value_date, COUNT(*) AS total
FROM measurements
GROUP BY value_date
ORDER BY value_date;
