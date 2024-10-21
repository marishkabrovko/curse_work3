from typing import Any


def get_employer_info(vacancy_data: dict[str, Any]) -> dict[str, Any]:
    """Получение словаря с данными о работадателе"""

    name = vacancy_data.get("employer").get("name")
    url = vacancy_data.get("employer").get("alternate_url")

    return {"name": name, "url": url}


def get_vacancy_info(vacancy_data: dict[str, Any]) -> dict[str, Any]:
    """Получение словаря с данными о вакансии"""

    name = vacancy_data.get("name")
    url = vacancy_data.get("alternate_url")

    if vacancy_data.get("salary"):

        if vacancy_data.get("salary").get("from"):
            salary_from = vacancy_data.get("salary").get("from")
        else:
            salary_from = 0

        if vacancy_data.get("salary").get("to"):
            salary_to = vacancy_data.get("salary").get("to")
        else:
            salary_to = 0

    else:
        salary_from = 0
        salary_to = 0

    return {
        "name": name,
        "salary_from": salary_from,
        "salary_to": salary_to,
        "url": url,
    }
