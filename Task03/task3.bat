#!/bin/bash
chcp 65001 2>/dev/null || true

sqlite3 movies_rating.db < db_init.sql

echo "1. Составить список фильмов, имеющих хотя бы одну оценку. Список фильмов отсортировать по году выпуска и по названиям. В списке оставить первые 10 фильмов."
echo --------------------------------------------------
sqlite3 movies_rating.db -box -echo "
SELECT DISTINCT m.id, m.title, m.year
FROM movies m
JOIN ratings r ON r.movie_id = m.id
ORDER BY m.year, m.title
LIMIT 10;
"
echo " "

echo "2. Вывести список всех пользователей, фамилии (не имена!) которых начинаются на букву 'A'. Полученный список отсортировать по дате регистрации. В списке оставить первых 5 пользователей."
echo --------------------------------------------------
sqlite3 movies_rating.db -box -echo "
SELECT id, name, register_date
FROM users
WHERE name LIKE '% A%'
ORDER BY register_date
LIMIT 5;
"
echo " "

echo "3. Информация о рейтингах: имя эксперта, название фильма, год, оценка, дата оценки (ГГГГ-ММ-ДД). Сортировка: имя, фильм, оценка. Первые 50 записей."
echo --------------------------------------------------
sqlite3 movies_rating.db -box -echo "
SELECT u.name AS expert, m.title, m.year, r.rating,
       date(r.timestamp, 'unixepoch') AS rating_date
FROM ratings r
JOIN users u ON u.id = r.user_id
JOIN movies m ON m.id = r.movie_id
ORDER BY u.name, m.title, r.rating
LIMIT 50;
"
echo " "

echo "4. Фильмы с тегами. Сортировка: год, название, тег. Первые 40 записей."
echo --------------------------------------------------
sqlite3 movies_rating.db -box -echo "
SELECT m.title, m.year, t.tag
FROM tags t
JOIN movies m ON m.id = t.movie_id
ORDER BY m.year, m.title, t.tag
LIMIT 40;
"
echo " "

echo "5. Самые свежие фильмы (все фильмы последнего года выпуска в БД)."
echo --------------------------------------------------
sqlite3 movies_rating.db -box -echo "
SELECT id, title, year
FROM movies
WHERE year = (SELECT MAX(year) FROM movies)
ORDER BY title;
"
echo " "

echo "6. Комедии после 2000 года, понравившиеся мужчинам (rating >= 4.5). Название, год, количество оценок. Сортировка: год, название."
echo --------------------------------------------------
sqlite3 movies_rating.db -box -echo "
SELECT m.title, m.year, COUNT(*) AS likes
FROM ratings r
JOIN movies m ON m.id = r.movie_id
JOIN users u ON u.id = r.user_id
WHERE m.genres LIKE '%Comedy%'
  AND m.year > 2000
  AND u.gender = 'male'
  AND r.rating >= 4.5
GROUP BY m.id, m.title, m.year
ORDER BY m.year, m.title;
"
echo " "

echo "7. Количество пользователей по профессиям."
echo --------------------------------------------------
sqlite3 movies_rating.db -box -echo "
SELECT occupation, COUNT(*) AS users_count
FROM users
GROUP BY occupation
ORDER BY users_count DESC;
"
echo " "

echo "Самая распространённая профессия:"
sqlite3 movies_rating.db -box -echo "
SELECT occupation, COUNT(*) AS cnt
FROM users
GROUP BY occupation
ORDER BY cnt DESC
LIMIT 1;
"
echo " "

echo "Самая редкая профессия:"
sqlite3 movies_rating.db -box -echo "
SELECT occupation, COUNT(*) AS cnt
FROM users
GROUP BY occupation
ORDER BY cnt ASC
LIMIT 1;
"
