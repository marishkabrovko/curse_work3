from typing import Any

import psycopg2


def create_db(db_name: str, params: dict[str, Any]) -> None:
    """Создание базы данных с необходимыми таблицами"""

    # создание базы данных
    conn = psycopg2.connect(dbname="postgres", **params)
    conn.autocommit = True

    with conn.cursor() as cur:
        try:
            cur.execute(f"DROP DATABASE IF EXISTS {db_name};")
        except psycopg2.errors.ObjectInUse:
            cur.execute(
                """
            SELECT pg_terminate_backend(pg_stat_activity.pid)
            FROM pg_stat_activity
            WHERE pg_stat_activity.datname = 'hh_ru'
            AND pid <> pg_backend_pid();"""
            )
            cur.execute(f"DROP DATABASE IF EXISTS {db_name};")

        cur.execute(f"CREATE DATABASE {db_name};")

    conn.close()

    # создание таблиц
    conn = psycopg2.connect(dbname=db_name, **params)

    with conn.cursor() as cur:
        cur.execute(
            """CREATE TABLE employers (
                employer_id SERIAL PRIMARY KEY,
                employer_name VARCHAR(255) NOT NULL,
                employer_url VARCHAR(255))"""
        )

    with conn.cursor() as cur:
        cur.execute(
            """CREATE TABLE vacancies (
                vacancy_id SERIAL PRIMARY KEY,
                employer_id INT REFERENCES employers(employer_id),
                vacancy_name VARCHAR(255) NOT NULL,
                salary_from FLOAT,
                salary_to FLOAT,
                url VARCHAR(255))"""
        )

    conn.commit()
    conn.close()
