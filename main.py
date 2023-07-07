import insert_and_update_table_for_emps
import insert_and_update_for_vacs
import psycopg2.errors

"""Скрипт для создания, заполнения и обновления таблиц
 с консольным интерфейсом"""

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
