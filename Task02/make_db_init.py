#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Генератор SQL-скрипта db_init.sql для создания и наполнения
базы данных movies_rating.db (SQLite).

Читает исходные файлы movies.csv, ratings.csv, tags.csv, users.txt,
лежащие в той же папке, что и скрипт.
"""

import csv
import os
import re


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_FILE = os.path.join(SCRIPT_DIR, "db_init.sql")


def esc(value):
    """Экранирует одинарные кавычки для SQL-строки."""
    return str(value).replace("'", "''")


def split_title_year(raw_title):
    """'Toy Story (1995)' -> ('Toy Story', 1995)."""
    m = re.search(r"\((\d{4})\)\s*$", raw_title)
    if m:
        year = int(m.group(1))
        title = raw_title[:m.start()].strip()
        return title, year
    return raw_title.strip(), None


def build_sql():
    lines = []
    lines.append("PRAGMA foreign_keys = OFF;")
    lines.append("BEGIN TRANSACTION;")
    lines.append("")

    lines.append("DROP TABLE IF EXISTS ratings;")
    lines.append("DROP TABLE IF EXISTS tags;")
    lines.append("DROP TABLE IF EXISTS movies;")
    lines.append("DROP TABLE IF EXISTS users;")
    lines.append("")

    # ----- movies -----
    lines.append(
        "CREATE TABLE movies (\n"
        "    id INTEGER PRIMARY KEY,\n"
        "    title TEXT NOT NULL,\n"
        "    year INTEGER,\n"
        "    genres TEXT\n"
        ");"
    )
    lines.append("")

    with open(os.path.join(SCRIPT_DIR, "movies.csv"),
              "r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            mid = int(row["movieId"])
            title, year = split_title_year(row["title"])
            genres = row["genres"]
            year_sql = str(year) if year is not None else "NULL"
            lines.append(
                "INSERT INTO movies (id, title, year, genres) "
                "VALUES ({}, '{}', {}, '{}');".format(
                    mid, esc(title), year_sql, esc(genres)
                )
            )
    lines.append("")

    # ----- ratings -----
    lines.append(
        "CREATE TABLE ratings (\n"
        "    id INTEGER PRIMARY KEY,\n"
        "    user_id INTEGER NOT NULL,\n"
        "    movie_id INTEGER NOT NULL,\n"
        "    rating REAL NOT NULL,\n"
        "    timestamp INTEGER NOT NULL\n"
        ");"
    )
    lines.append("")

    with open(os.path.join(SCRIPT_DIR, "ratings.csv"),
              "r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            uid = int(row["userId"])
            mid = int(row["movieId"])
            rating = float(row["rating"])
            ts = int(row["timestamp"])
            lines.append(
                "INSERT INTO ratings (user_id, movie_id, rating, timestamp) "
                "VALUES ({}, {}, {}, {});".format(uid, mid, rating, ts)
            )
    lines.append("")

    # ----- tags -----
    lines.append(
        "CREATE TABLE tags (\n"
        "    id INTEGER PRIMARY KEY,\n"
        "    user_id INTEGER NOT NULL,\n"
        "    movie_id INTEGER NOT NULL,\n"
        "    tag TEXT NOT NULL,\n"
        "    timestamp INTEGER NOT NULL\n"
        ");"
    )
    lines.append("")

    with open(os.path.join(SCRIPT_DIR, "tags.csv"),
              "r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            uid = int(row["userId"])
            mid = int(row["movieId"])
            tag = row["tag"]
            ts = int(row["timestamp"])
            lines.append(
                "INSERT INTO tags (user_id, movie_id, tag, timestamp) "
                "VALUES ({}, {}, '{}', {});".format(uid, mid, esc(tag), ts)
            )
    lines.append("")

    # ----- users -----
    lines.append(
        "CREATE TABLE users (\n"
        "    id INTEGER PRIMARY KEY,\n"
        "    name TEXT NOT NULL,\n"
        "    email TEXT,\n"
        "    gender TEXT,\n"
        "    register_date TEXT,\n"
        "    occupation TEXT\n"
        ");"
    )
    lines.append("")

    with open(os.path.join(SCRIPT_DIR, "users.txt"),
              "r", encoding="utf-8") as f:
        for raw in f:
            raw = raw.rstrip("\r\n")
            if not raw:
                continue
            parts = raw.split("|")
            if len(parts) < 6:
                continue
            uid = int(parts[0])
            name = parts[1]
            email = parts[2]
            gender = parts[3]
            date = parts[4]
            occ = parts[5]
            lines.append(
                "INSERT INTO users (id, name, email, gender, "
                "register_date, occupation) "
                "VALUES ({}, '{}', '{}', '{}', '{}', '{}');".format(
                    uid, esc(name), esc(email), esc(gender),
                    esc(date), esc(occ)
                )
            )
    lines.append("")
    lines.append("COMMIT;")
    return "\n".join(lines) + "\n"


def main():
    sql = build_sql()
    with open(OUTPUT_FILE, "w", encoding="utf-8", newline="\n") as f:
        f.write(sql)
    print("Сгенерирован файл: {}".format(OUTPUT_FILE))


if __name__ == "__main__":
    main()
