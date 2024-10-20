from abc import ABC, abstractmethod

import requests


class Parser(ABC):
    """Aбстрактный класс для парсинга"""

    @abstractmethod
    def load_vacancies(self, employer_id: str) -> list[dict]:
        """Получение вакансий с по API"""
        pass


class HeadHunterAPI(Parser):
    """Класс для работы с API HeadHunter"""

    def __init__(self) -> None:
        """Инициализатор класса HeadHunterAPI"""
        self.__url: str = "https://api.hh.ru/vacancies"
        self.__headers: dict[str, str] = {"User-Agent": "HH-User-Agent"}
        self.__params: dict[str, int] = {"employer_id": "", "page": 0, "per_page": 100}
        self.__vacancies: list[dict] = []

    def __api_connect(self) -> requests.Response:
        """Подключение к API hh.ru"""
        response = requests.get(self.__url, headers=self.__headers, params=self.__params)
        if response.status_code == 200:
            return response

        print("Ошибка получения данных")

    def load_vacancies(self, employer_id: str) -> list:
        """Получение вакансий с hh.ru"""

        self.__params["employer_id"] = employer_id
        while self.__params.get("page") != 5:
            response = self.__api_connect()
            if response:
                vacancies = response.json()["items"]
                self.__vacancies.extend(vacancies)
                self.__params["page"] += 1
            else:
                break

        return self.__vacancies
