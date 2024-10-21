from config import config
from src.database_creator import create_db
from src.db_manager import DBManager
from src.head_hunter_api import HeadHunterAPI
from src.tables_filler import enter_data_into_tables
from src.utils import get_employer_info, get_vacancy_info


def main(employers_names: list[str]) -> None:
    print("Здравствуйте, программа запущена!")
    print("Начинаю загрузку вакансий с сайта hh.ru\nПожалуйста, подождите...\n")

    # создание базы данных
    params = config()
    create_db("hh_ru", params)

    # загрузка вакансий
    for employer in employers_names:
        vacancies_info = HeadHunterAPI().load_vacancies(employer)

        employer_data = get_employer_info(vacancies_info[0])
        vacancies_data = [get_vacancy_info(vacancy) for vacancy in vacancies_info]

        enter_data_into_tables("hh_ru", params, employer_data, vacancies_data)

    manager = DBManager("hh_ru", params)

    # отображение общей информауии о полученных данных
    print("Получены вакансии:")
    for data in manager.get_companies_and_vacancies_count():
        print(data)

    # выбор ползователем необходимого действия
    print("\nКакую информацию вы хотите получить?\n")
    print("1. Средняя зарплата по вакансиям;")
    print("2. Вакансии, у которых зарплата выше средней;")
    print("3. Вакансии по ключевому слову в названии;")
    print("4. Все вакансии.\n")

    try:
        choice = int(input("Введите цифру от 1 до 4: "))
    except ValueError:
        print("Некорректный ввод. Выбрано действие 4\n")
        choice = 4
    else:
        if choice not in range(1, 5):
            print("Некорректный ввод. Выбрано действие 4")
            choice = 4

    # отображения информации согласно выбору пользователя
    print()
    if choice == 1:
        print(manager.get_avg_salary())

    elif choice == 2:
        for vac in manager.get_vacancies_with_higher_salary():
            print(vac)

    elif choice == 3:
        keyword = input("Введите слово для поиска: ").lower()
        vacs = manager.get_vacancies_with_keyword(keyword)
        if vacs:
            for vac in manager.get_vacancies_with_keyword(keyword):
                print(vac)
        else:
            print(f"Вакансий по запросу {keyword} не обнаружено")

    else:
        for vac in manager.get_all_vacancies():
            print(vac)

    print("\nПрограмма завершена")
    print("До свидания!☺")


if __name__ == "__main__":
    employers = ["78638", "3529", "80", "981", "68587", "1322149", "127256",
                 "818312", "2739158", "644105"]

    main(employers)
