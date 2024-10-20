from typing import Any

import psycopg2


class DBManager:
    """Класс для получения ифнормации о вакансиях из базы данных"""

    def __init__(self, db_name: str, params: dict[str, Any]) -> None:
        """Инициализато класса DBManager"""
        self.db_name = db_name
        self.__params = params

    def __connect_database(self):
        """Подключение к базе данных"""
        return psycopg2.connect(dbname=self.db_name, **self.__params)

    def get_companies_and_vacancies_count(self) -> list[str]:
        """Возвращает список работодателей и количество вакансий"""
        conn = self.__connect_database()
        with conn.cursor() as cur:
            cur.execute(
                """SELECT employers.employer_name, COUNT(*)
                FROM vacancies JOIN employers USING(employer_id)
                GROUP BY employers.employer_name;"""
            )
            vacs_counter = cur.fetchall()

        conn.close()

        return [f"{employer[0]}: {employer[1]} вакансий" for employer in vacs_counter]

    def get_all_vacancies(self) -> list[str]:
        """Возвращает список всех вакансий"""
        conn = self.__connect_database()
        with conn.cursor() as cur:
            cur.execute(
                """SELECT employers.employer_name, vacancy_name, salary_from, salary_to, vacancies.url
            FROM vacancies JOIN employers USING(employer_id);"""
            )
            vacs_data = cur.fetchall()

        conn.close()

        result = []

        for vac in vacs_data:
            if vac[2] == 0.0 and vac[3] == 0.0:
                result.append(f"-={vac[0]}=-, вакансия: {vac[1]}\nЗарплата: не указана. Ссылка: {vac[4]}\n")
            elif vac[3] == 0.0:
                result.append(f"-={vac[0]}=-, вакансия: {vac[1]}\nЗарплата: от {vac[2]}. Ссылка: {vac[4]}\n")
            elif vac[2] == 0.0:
                result.append(f"-={vac[0]}=-, вакансия: {vac[1]}\nЗарплата: до {vac[3]}. Ссылка: {vac[4]}\n")
            else:
                result.append(f"-={vac[0]}=-, вакансия: {vac[1]}\nЗарплата: {vac[2]} - {vac[3]}. Ссылка: {vac[4]}\n")

        return result

    def get_avg_salary(self) -> str:
        """Возвращает среднюю зарплату по вакансиям"""
        conn = self.__connect_database()
        with conn.cursor() as cur:
            cur.execute("""SELECT AVG(salary_from) FROM vacancies;""")
            salary_from = round(cur.fetchone()[0])

            cur.execute("""SELECT AVG(salary_to) FROM vacancies;""")
            salary_to = round(cur.fetchone()[0])

        conn.close()

        return f"Средняя зарплата: {salary_from} - {salary_to}"

    def get_vacancies_with_higher_salary(self) -> list[str]:
        """Возвращает список вакансий, у которых зарплата выше средней"""
        conn = self.__connect_database()
        with conn.cursor() as cur:
            cur.execute("""SELECT AVG(salary_to) FROM vacancies;""")
            avg_salary = round(cur.fetchone()[0])

            cur.execute(
                f"SELECT vacancy_name, salary_from, salary_to, url FROM vacancies "
                f"WHERE salary_from > {avg_salary} OR salary_to > {avg_salary};"
            )

            vacs = cur.fetchall()

        conn.close()

        result = []

        for vac in vacs:
            if vac[1] == 0.0:
                result.append(f"• {vac[0]}\nЗарплата: до {vac[2]}. Ссылка: {vac[3]}\n")
            elif vac[2] == 0.0:
                result.append(f"• {vac[0]}\nЗарплата: от {vac[1]}. Ссылка: {vac[3]}\n")
            else:
                result.append(f"• {vac[0]}\nЗарплата: {vac[1]} - {vac[2]}. Ссылка: {vac[3]}\n")

        return result

    def get_vacancies_with_keyword(self, keyword: str) -> list[str]:
        """Возвращает список вакансий по ключевому слову в названии"""
        conn = self.__connect_database()
        with conn.cursor() as cur:
            cur.execute(
                f"SELECT vacancy_name, salary_from, salary_to, url FROM vacancies "
                f"WHERE vacancy_name iLIKE '%{keyword}%';"
            )
            vacs = cur.fetchall()

        conn.close()

        result = []

        for vac in vacs:
            if vac[1] == 0 and vac[2] == 0:
                result.append(f"• {vac[0]}\nЗарплата: не указана. Ссылка: {vac[3]}\n")
            elif vac[2] == 0:
                result.append(f"• {vac[0]}\nЗарплата: от {vac[1]}. Ссылка: {vac[3]}\n")
            elif vac[1] == 0:
                result.append(f"• {vac[0]}\nЗарплата: до {vac[2]}. Ссылка: {vac[3]}\n")
            else:
                result.append(f"• {vac[0]}\nЗарплата: {vac[1]} - {vac[2]}. Ссылка: {vac[3]}\n")

        return result
