import insert_and_update_table_for_emps
import insert_and_update_for_vacs
import psycopg2.errors
from DBManager import *

"""Скрипт для создания, заполнения и обновления таблиц
 с консольным интерфейсом"""


def Manager(port, host, user, database, password):
    M = UserDBManager()

    while True:
        print("""Выберите интересующий метод и введите цифру, соответствующую ему:
              1: Вывести список компаний и количество вакансий у каждой из них.
              2: Вывести список всех вакансий.
              3: Вывести среднюю зарплату.
              4: Вывести вакансии, зарплата которых выше средней.
              5: Вывести все вакансии по ключевому слову.
              0: Завершить работу.""", end = ": ")
        user_choice = input()
        if user_choice in ["0", "1", "2", "3", "4", "5"]:
            if user_choice == "0":
                print("Завершаю работу...")
                exit()
            elif user_choice == "1":
                M.User_CnV_count(port, host, user, database, password)
            elif user_choice == "2":
                M.User_all_vacs(port, host, user, database, password)
            elif user_choice == "3":
                M.User_avg(port, host, user, database, password)
            elif user_choice == "4":
                M.User_higher(port, host, user, database, password)
            else:
                keyword = input("Введите ключевое слово: ")
                M.User_keyword(port, host, user, database, password, keyword)


def UserInteraction():
    print("Добрый день! Введите, пожалуйста, данные для"
          "подключения к вашему postgres серверу:")

    port = input("Порт (по умолчанию - 1433): ")
    if port == "":
        port = "1433"

    host = input("Хост (по умолчанию - localhost): ")
    if host == "":
        host = "localhost"

    user = input("Имя пользователя (по умолчанию - postgres): ")
    if user == "":
        user = "postgres"

    database = input("Название вашей БД: ")
    password = input("Пароль: ")

    try:
        while True:
            print("В этой базе данных уже есть таблицы vacancies и "
                  "employers? (Введите 1 - если да и 0 - если нет)")
            answer = input()
            if answer in ("0", "1"):
                break
            else:
                print("Пожалуйста, введите 0 или 1")

        if answer == "1":
            print("Обновляю вашу таблицу. Это может занять некоторое количество времени...")
            insert_and_update_table_for_emps.insert_into_table(port, host, user, database, password)
            insert_and_update_for_vacs.insert_into_table(port, host, user, database, password)
            print("Таблицы обновлены!")

            Manager(port, host, user, database, password)
        else:
            print("Создаю таблицы на вашей базе данных...")
            try:
                insert_and_update_for_vacs.create_table(port, host, user, database, password)
                insert_and_update_table_for_emps.create_table(port, host, user, database, password)

                insert_and_update_for_vacs.insert_into_table(port, host, user, database, password)
                insert_and_update_table_for_emps.insert_into_table(port, host, user, database, password)
                print("Таблицы созданы!")
            except psycopg2.errors.DuplicateTable:
                print("Таблицы с таким названием уже существуют в вашей базе данных!")

    except psycopg2.OperationalError:
        print("Какие-то данные были введены неверно:(")


if __name__ == "__main__":
    UserInteraction()
